"""
Meta-Cognition: Draft -> Critic -> Rewrite -> Choose.

Phase 2 Refactoring Insight:
  Current: Critic just scores draft
  Future: CritiqueReport with {confidence, fact_error, belief_conflict,
          memory_conflict, missing_information, style_issue, reasoning_gap}
  
  Meta decides WHICH issues to fix (not just binary rewrite yes/no).
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from bio_agent_v4.interfaces.shared import (
    MetaCognitionResult,
    PredictionError,
    UncertaintyState,
    ExecutiveDecision,
)


class CriticEngine(ABC):
    """
    Evaluate draft response for errors & issues.
    
    Input:  Draft response + WorldModel snapshot + recent PredictionError
    Output: Confidence score [0..1] + list of issues found
    State:  None (stateless; can call LLM for deep critique)
    Clock:  Each turn if budget >= MEDIUM
    
    Events:
        emit:   "critic_evaluated" {confidence, issues}
        listen: (called from MetaCognitionEngine before rewrite decision)
    
    Latency: ~0.1 ms (if using heuristics) or ~100 ms (if calling LLM)
    
    Phase 2 Design:
      Critic doesn't just return 0.7 (confidence).
      Returns structured CritiqueReport:
        - confidence: 0.0-1.0
        - fact_errors: [{claim, counterevidence}, ...]
        - belief_conflicts: [{claim, conflicting_belief}, ...]
        - memory_conflicts: [{claim, contradicts_history}, ...]
        - missing_information: [question1, question2, ...]
        - style_issues: [{issue_type, suggestion}, ...]
        - reasoning_gaps: [gap1, gap2, ...]
    """

    @abstractmethod
    def critique(self, draft: str, world_snapshot: Dict,
                 recent_pe: Optional[PredictionError]) -> tuple[float, List[Dict]]:
        """
        Analyze draft for errors.
        
        Args:
            draft: The generated response
            world_snapshot: Current world model state
            recent_pe: Most recent prediction error (if any)
        
        Returns:
            (confidence: float, issues: List[{type, description, severity}])
        """
        ...

    @abstractmethod
    def fact_check(self, draft: str, world_snapshot: Dict) -> List[Dict]:
        """
        Check claims against known beliefs.
        
        Args:
            draft: Response to check
            world_snapshot: Known facts
        
        Returns:
            List of {claim, status, counterevidence} dicts
        """
        ...

    @abstractmethod
    def detect_hallucination(self, draft: str, world_snapshot: Dict) -> bool:
        """
        Does draft claim things we don't know (possible hallucination)?
        
        Args:
            draft: Response to check
            world_snapshot: Known facts
        
        Returns:
            True if hallucination suspected
        """
        ...


class MetaCognitionEngine(ABC):
    """
    Meta-cognitive loop: Draft -> Critic -> Decide Rewrite -> Finalize.
    
    Input:  Draft (from Planner/LLM) + Critic output + ExecutiveDecision
    Output: MetaCognitionResult with final response
    State:  Rewrite count limiter (prevent infinite loops)
    Clock:  Each turn if budget >= MEDIUM
    
    Events:
        emit:   "response_finalized" {result}
        listen: "draft_ready" (from Planner)
    
    Latency: ~0.2 ms (heuristic) or ~200 ms (LLM rewrite)
    
    IMPORTANT:
      - Memory is written ONLY for final_response (not draft or rewrites)
      - This ensures episodic memory captures tested, vetted responses
    """

    @abstractmethod
    def should_rewrite(self, confidence: float, pe: Optional[PredictionError],
                       uncertainty: Optional[UncertaintyState]) -> bool:
        """
        Decide if rewrite is needed.
        
        Args:
            confidence: Critic's confidence [0..1]
            pe: Recent prediction error (if any)
            uncertainty: Current uncertainty state (if any)
        
        Returns:
            True if rewrite warranted
        """
        ...

    @abstractmethod
    def rewrite(self, draft: str, critique_issues: List[Dict],
                executive_decision: ExecutiveDecision) -> str:
        """
        Generate improved response based on critique.
        
        Args:
            draft: Original response
            critique_issues: List of issues from Critic
            executive_decision: Context about goal/mode
        
        Returns:
            Rewritten response
        """
        ...

    @abstractmethod
    def run(self, draft: str, world_snapshot: Dict,
            executive_decision: ExecutiveDecision,
            recent_pe: Optional[PredictionError] = None) -> MetaCognitionResult:
        """
        Full meta-cognitive pipeline.
        
        Args:
            draft: Initial response
            world_snapshot: Current world model
            executive_decision: Context & goal
            recent_pe: Recent error (optional)
        
        Returns:
            MetaCognitionResult with final response & metadata
        """
        ...

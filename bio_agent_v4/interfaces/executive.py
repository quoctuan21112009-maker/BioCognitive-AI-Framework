"""
Executive Controller: Minimal interface using DecisionContext bottleneck.

Phase 2 Refactoring Insight:
  Current: Executive reads 6+ modules (World, Need, Hormone, Trait, etc.)
  Future: Executive ONLY reads DecisionContext
  
  All other modules populate DecisionContext with exactly what Executive needs.
  This is THE critical refactoring to avoid God Module.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from bio_agent_v4.interfaces.shared import (
    DecisionContext,
    ExecutiveDecision,
    NeedState,
)


class ExecutiveController(ABC):
    """
    Goal selection, conflict resolution, inhibition, task switching, planning horizon.
    
    Input:  DecisionContext (ONLY this; bottleneck pattern)
    Output: ExecutiveDecision
    State:  goal_stack (for task switching), error_log (recent PE)
    Clock:  Every turn after MotivationNetwork
    
    Events:
        emit:   "executive_decision_made" {decision}
        listen: "motivation_updated"
    
    Latency: ~0.05 ms
    
    CRITICAL DESIGN (Phase 2):
      Executive does NOT read:
        - WorldModel directly (only via DecisionContext.world_focus)
        - Need graph directly (only via DecisionContext.dominant_need)
        - Uncertainty directly (only via DecisionContext.uncertainty)
        - Hormone/Trait (not used at this layer)
      
      All context needed is in DecisionContext. If Executive needs something new,
      ADD IT TO DecisionContext, don't add new module reads.
    """

    @abstractmethod
    def select_goal(self, candidates: List[str], dominant_need: NeedState) -> str:
        """
        Choose primary goal from candidates.
        
        Args:
            candidates: List of possible goals
            dominant_need: Current strongest need (for bias)
        
        Returns:
            Selected goal
        """
        ...

    @abstractmethod
    def resolve_conflict(self, goal_a: str, goal_b: str,
                        context: DecisionContext) -> str:
        """
        When two goals conflict, choose the winner.
        
        Uses uncertainty, prediction error, and need alignment.
        
        Args:
            goal_a: First goal
            goal_b: Second goal
            context: Full context for arbitration
        
        Returns:
            Winning goal
        """
        ...

    @abstractmethod
    def push_goal(self, goal: str) -> None:
        """
        Push goal onto stack (task switching: suspend current, pursue new).
        
        Args:
            goal: Goal to push
        """
        ...

    @abstractmethod
    def pop_goal(self) -> Optional[str]:
        """
        Pop goal from stack (resume previous task after interlude).
        
        Returns:
            Popped goal or None if stack empty
        """
        ...

    @abstractmethod
    def current_goal(self) -> Optional[str]:
        """
        Get the current (top-of-stack) goal.
        
        Returns:
            Current goal or None
        """
        ...

    @abstractmethod
    def monitor_errors(self, context: DecisionContext) -> bool:
        """
        Check if recent errors warrant escalation to Meta-Cognition.
        
        Returns True if uncertainty or PE high enough to trigger meta-cog.
        
        Args:
            context: Current decision context with error_signal
        
        Returns:
            True if meta-cognition should be triggered
        """
        ...

    @abstractmethod
    def decide(self, context: DecisionContext) -> ExecutiveDecision:
        """
        Make executive decision using ONLY the provided context.
        
        Args:
            context: DecisionContext with all needed information
        
        Returns:
            ExecutiveDecision with goal, conflicts, inhibitions, horizon, mode
        """
        ...

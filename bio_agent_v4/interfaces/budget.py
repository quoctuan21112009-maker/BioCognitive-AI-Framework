"""
Cognitive Budget Manager: Route to FAST/MEDIUM/DEEP.

Routing decision BEFORE main pipeline (first thing called each turn).
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple
from bio_agent_v4.interfaces.shared import CognitiveBudget, UncertaintyState


class CognitiveBudgetManager(ABC):
    """
    Route each turn to FAST/MEDIUM/DEEP pipeline.
    
    Input:  Raw input + recent history + uncertainty state
    Output: (CognitiveBudget, reason_string)
    State:  Rolling stats on input complexity & patterns
    Clock:  Every turn, FIRST before anything else
    
    Events:
        emit:   "budget_decided" {budget, reason}
        listen: "input_received"
    
    Latency: ~0.05 ms
    
    Decision Rules (heuristics):
      FAST: simple input (e.g., "2+2=") OR very low complexity pattern
            -> skip Refined Attention, WorldModel write, Prediction, Meta
            -> go straight CheapAttention(rut gon) -> Planner -> LLM
      
      MEDIUM: moderate complexity OR pattern change detected
              -> include WorldModel + Prediction, skip Meta/deep-sleep
      
      DEEP: high uncertainty OR high PE OR user confusion detected
            -> full pipeline including Meta-Cognition
    
    Goal: Most turns are FAST (simple), occasional MEDIUM/DEEP for complex cases.
    """

    @abstractmethod
    def decide(self, raw_input: str, uncertainty: Optional[UncertaintyState],
               dev_stage: str) -> Tuple[CognitiveBudget, str]:
        """
        Decide budget routing.
        
        Args:
            raw_input: Current user message
            uncertainty: Current UncertaintyState (if available from t-1)
            dev_stage: Development stage (affects planning_horizon)
        
        Returns:
            (CognitiveBudget enum, reason_string for debugging)
        """
        ...

    @abstractmethod
    def is_simple_pattern(self, raw_input: str) -> bool:
        """
        Heuristic: does this look like a simple, stereotyped input?
        
        Examples: "2+2=", "what time is it?", "hi"
        
        Args:
            raw_input: Input to check
        
        Returns:
            True if pattern matches simple templates
        """
        ...

    @abstractmethod
    def is_high_uncertainty(self, uncertainty: Optional[UncertaintyState]) -> bool:
        """
        Check if uncertainty warrants deeper processing.
        
        Args:
            uncertainty: Current state (or None if N/A)
        
        Returns:
            True if variance/trend indicates need for DEEP
        """
        ...

    @abstractmethod
    def update_complexity_stats(self, raw_input: str, was_correct: bool) -> None:
        """
        Learn: track which input patterns led to correct predictions.
        
        Used to refine simple_pattern() heuristic over time.
        
        Args:
            raw_input: The input
            was_correct: Did our prediction about it succeed?
        """
        ...

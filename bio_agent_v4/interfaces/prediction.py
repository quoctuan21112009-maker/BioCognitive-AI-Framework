"""
Prediction & Error Analysis: Multi-dimensional with credit assignment.

Phase 2 Refactoring Insight:
  Current: Prediction returns single PE score
  Future: Decompose error to {world_error, planner_error, memory_error, prediction_error, llm_error}
  
  This allows Genome to know WHICH module to update.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from bio_agent_v4.interfaces.shared import (
    PredictionResult,
    PredictionError,
    UncertaintyState,
)


class PredictionEngine(ABC):
    """
    Multi-output prediction: sentiment, followup, confidence, goal, info_gain.
    
    Input:  WorldModel snapshot + internal state (traits, hormones from v3)
    Output: PredictionResult (struct, NOT single score)
    State:  Buffer of pending predictions (different resolution latencies)
    Clock:  Every turn before LLM (if budget >= MEDIUM)
    
    Events:
        emit:   "prediction_made" {result, prediction_id}
        listen: "world_model_updated"
    
    Latency: ~0.2 ms
    
    Key Design:
      - Sentiment usually resolves same turn (immediate user reaction)
      - Followup/goal may need 2-10 turns to resolve
      - Each dimension tracked separately in pending buffer
    """

    @abstractmethod
    def predict_conversation_outcome(self, world_snapshot: Dict,
                                      internal_state: Dict) -> PredictionResult:
        """
        Generate full prediction for this turn.
        
        Args:
            world_snapshot: Output from WorldModel.snapshot()
            internal_state: Traits, hormones, attention state (from v3)
        
        Returns:
            PredictionResult with all 5 dimensions
        """
        ...

    @abstractmethod
    def register_pending(self, result: PredictionResult) -> str:
        """
        Queue prediction for later resolution.
        
        Args:
            result: The prediction to track
        
        Returns:
            prediction_id for later reference
        """
        ...

    @abstractmethod
    def try_resolve_pending(self, actual_signals: Dict) -> List[Tuple[str, PredictionResult]]:
        """
        Check if any pending predictions can be resolved.
        
        Called each turn; returns newly-resolved predictions.
        
        Args:
            actual_signals: Observed outcomes
              - sentiment: user reaction (positive/negative/neutral)
              - followup_topic: did user continue on same topic?
              - goal_progress: did the goal advance?
              - info_from_response: how much new information?
        
        Returns:
            List of (prediction_id, resolved_PredictionResult) tuples
        """
        ...

    @abstractmethod
    def get_pending_count(self) -> int:
        """
        How many predictions still awaiting resolution?
        
        Returns:
            Count of pending predictions
        """
        ...


class PredictionErrorEngine(ABC):
    """
    Compute error AND attribute to responsible module.
    
    Input:  Resolved PredictionResult + actual observed signals
    Output: PredictionError (4 main dims + 5 attribution dims)
    State:  None (pure function)
    Clock:  Event-driven (when prediction resolves)
    
    Events:
        emit:   "prediction_error_computed" {error, prediction_id}
        listen: (called directly from PredictionEngine, not via bus)
    
    Latency: ~0.05 ms
    
    Key Design (Phase 2):
      - Not just |predicted - actual|, but WHICH module failed?
      - world_error: Did world model misrepresent state?
      - planner_error: Did planner choose bad action?
      - memory_error: Did context/memory cause confusion?
      - prediction_error: Did predictor itself miscalibrate?
      - llm_error: Did LLM generate suboptimal response?
    """

    @abstractmethod
    def compute(self, predicted: PredictionResult, actual: Dict) -> PredictionError:
        """
        Compute error with attribution.
        
        Args:
            predicted: What was predicted
            actual: What actually happened
        
        Returns:
            PredictionError with main dimensions + attributions
        """
        ...

    @abstractmethod
    def attribute_error(self, error: PredictionError, context: Dict) -> Dict[str, float]:
        """
        Deep dive: which module is responsible?
        
        Uses heuristics & historical data to assign blame.
        
        Args:
            error: The computed error
            context: Additional context (world state, planner output, etc.)
        
        Returns:
            {module_name: responsibility_fraction}
            e.g., {'world': 0.3, 'planner': 0.2, 'llm': 0.5}
        """
        ...


class UncertaintyEngine(ABC):
    """
    Rolling statistics on prediction errors.
    
    Input:  New PredictionError + rolling history per context
    Output: UncertaintyState (mean/var/trend PE)
    State:  Dict[context] -> rolling list of recent PE (e.g., last 20)
    Clock:  Event-driven (each PredictionError)
    
    Events:
        emit:   "uncertainty_updated" {state, context}
        listen: "prediction_error_computed"
    
    Latency: ~0.05 ms
    
    Decision Rule:
      variance_pe HIGH + trend_pe RISING -> mode = "explore"
      variance_pe LOW + mean_pe LOW -> mode = "exploit"
    
    Used by:
      - CognitiveBudgetManager (high uncertainty -> more compute)
      - MotivationNetwork (explore needs boost uncertainty)
      - MetaCognitionEngine (high uncertainty -> stricter critic)
      - SleepEngine (high uncertainty -> more counterfactual dreaming)
    """

    @abstractmethod
    def update(self, context: str, pe: PredictionError) -> UncertaintyState:
        """
        Add new error observation, compute rolling stats.
        
        Args:
            context: Context bucket ('belief', 'goal', 'conversation', ...)
            pe: New prediction error
        
        Returns:
            Updated UncertaintyState for this context
        """
        ...

    @abstractmethod
    def get(self, context: str) -> UncertaintyState:
        """
        Retrieve current uncertainty state for context.
        
        Args:
            context: Context to query
        
        Returns:
            UncertaintyState (or default if context new)
        """
        ...

    @abstractmethod
    def get_all(self) -> Dict[str, UncertaintyState]:
        """
        Get all contexts' uncertainty states.
        
        Returns:
            Dict[context_name -> UncertaintyState]
        """
        ...

    @abstractmethod
    def decide_mode(self, context: str) -> str:
        """
        Compute explore vs exploit mode for context.
        
        Args:
            context: Context to evaluate
        
        Returns:
            'explore' or 'exploit'
        """
        ...

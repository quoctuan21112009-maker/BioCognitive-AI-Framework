"""
Memory Encoder: Importance weighting & consolidation trigger.

Phase 2 Refactoring Insight:
  Current: importance = emotion × novelty × PE × uncertainty
  Future: importance = w1*emotion + w2*novelty + w3*PE + w4*uncertainty + w5*goal_relevance
  
  Avoids zero-out when any component is 0.
"""

from abc import ABC, abstractmethod
from typing import Optional
from bio_agent_v4.interfaces.shared import (
    EmotionEstimate,
    PredictionError,
    UncertaintyState,
    MemoryImportanceWeights,
)


class MemoryEncoder(ABC):
    """
    Compute importance weight & trigger consolidation.
    
    Input:  Final response + EmotionEstimate + novelty + PredictionError + UncertaintyState
    Output: importance_weight [0..1] + episode_id
    State:  None (reads v3's Storage, writes through it)
    Clock:  Each turn after MetaCognition
    
    Events:
        emit:   "memory_encoded" {weight, episode_id}
        listen: "response_finalized"
    
    Latency: ~0.05 ms
    
    Phase 2 Design:
      Weighted sum instead of product:
        importance = w_emotion*emotion + w_novelty*novelty + w_pe*pe +
                     w_uncertainty*uncertainty + w_goal_relevance*goal_rel
      
      Weights tunable via MemoryImportanceWeights dataclass.
      Default: emotion=0.25, novelty=0.25, pe=0.25, uncertainty=0.15, goal=0.10
    """

    @abstractmethod
    def compute_importance(self, emotion: Optional[EmotionEstimate],
                           novelty: float,
                           pe: Optional[PredictionError],
                           uncertainty: Optional[UncertaintyState],
                           goal_relevance: float) -> float:
        """
        Compute memory importance using weighted sum.
        
        Args:
            emotion: User's emotional state (if available)
            novelty: How novel was the exchange [0..1]
            pe: Prediction error (if available)
            uncertainty: Current uncertainty (if available)
            goal_relevance: How relevant to current goal [0..1]
        
        Returns:
            Importance weight [0..1]
        """
        ...

    @abstractmethod
    def encode(self, final_response: str, importance: float,
               metadata: dict = None) -> str:
        """
        Store response in memory system.
        
        Args:
            final_response: The response to encode
            importance: Weight [0..1] determining storage depth
            metadata: Optional metadata (goal, emotion, etc.)
        
        Returns:
            episode_id for later reference
        """
        ...

    @abstractmethod
    def get_weights(self) -> MemoryImportanceWeights:
        """
        Retrieve current weight configuration.
        
        Returns:
            MemoryImportanceWeights instance
        """
        ...

    @abstractmethod
    def set_weights(self, weights: MemoryImportanceWeights) -> None:
        """
        Update weight configuration (for tuning/meta-learning).
        
        Args:
            weights: New weight configuration
        """
        ...

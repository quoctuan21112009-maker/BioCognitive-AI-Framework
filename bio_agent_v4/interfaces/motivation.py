"""
Motivation Network: Need graph with lateral inhibition.

Phase 2 Refactoring Insight:
  Current: Motivations as simple list of scores
  Future: Needs as graph with inhibition (Safety inhibits Curiosity when danger high)
  
  Instead of: motivation_scores = [safety=0.3, curiosity=0.9, affiliation=0.5]
  Model: NeedState with inhibition propagation
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from bio_agent_v4.interfaces.shared import NeedState, UncertaintyState


class MotivationNetwork(ABC):
    """
    Competitive need activation with inhibition.
    
    Input:  UncertaintyState, Hormone snapshot (v3), WorldModel intents
    Output: dominant_need (the "winning" need after inhibition)
    State:  Dict[need_name] -> NeedState with inhibition matrix
    Clock:  Every turn after Uncertainty updates
    
    Events:
        emit:   "motivation_updated" {dominant_need, all_needs}
        listen: "uncertainty_updated"
    
    Latency: ~0.05 ms
    
    Key Design:
      - NOT sum of motivations (max(scores))
      - Lateral inhibition: high Safety suppresses Curiosity
      - Refractory period: if need satisfied recently, activation drops
      - Novelty & uncertainty BOOST Curiosity (exploration needs)
      - Memory conflicts BOOST Safety (caution needs)
    """

    @abstractmethod
    def set_need_level(self, need_name: str, level: float) -> None:
        """
        Set base activation level for a need.
        
        Args:
            need_name: 'Safety', 'Curiosity', 'Affiliation', 'Achievement', ...
            level: Activation [0..1]
        """
        ...

    @abstractmethod
    def set_inhibition(self, inhibitor: str, inhibited: str, strength: float) -> None:
        """
        Define inhibitory connection.
        
        Example: set_inhibition('Safety', 'Curiosity', 0.8)
        -> When Safety=0.9, Curiosity activation reduced by 0.9*0.8
        
        Args:
            inhibitor: Need that does inhibiting
            inhibited: Need that gets suppressed
            strength: Inhibition strength [0..1]
        """
        ...

    @abstractmethod
    def propagate_inhibition(self, iterations: int = 1) -> None:
        """
        Compute one step of lateral inhibition.
        
        Each iteration: inhibited_need.level -= inhibitor.level * inhibition_strength
        Repeat until convergence or fixed iterations.
        
        Args:
            iterations: How many rounds of propagation
        """
        ...

    @abstractmethod
    def update_from_uncertainty(self, uncertainty: UncertaintyState) -> None:
        """
        Boost needs based on uncertainty state.
        
        High uncertainty + explore mode -> boost Curiosity
        High uncertainty + exploit mode -> boost Safety
        
        Args:
            uncertainty: Current UncertaintyState
        """
        ...

    @abstractmethod
    def satisfy_need(self, need_name: str) -> None:
        """
        Mark a need as satisfied (e.g., Affiliation satisfied after social exchange).
        
        Sets refractory period during which activation stays low.
        
        Args:
            need_name: Which need to satisfy
        """
        ...

    @abstractmethod
    def dominant_need(self) -> NeedState:
        """
        Get the highest-activation need after inhibition & refractory.
        
        Returns:
            The "winning" NeedState
        """
        ...

    @abstractmethod
    def snapshot(self) -> Dict[str, float]:
        """
        Get all needs' current activation levels.
        
        Returns:
            Dict[need_name -> activation]
        """
        ...

    @abstractmethod
    def get_need(self, need_name: str) -> Optional[NeedState]:
        """
        Retrieve a specific need's state.
        
        Args:
            need_name: Name of need
        
        Returns:
            NeedState or None if not found
        """
        ...

"""
Sleep Engine: Replay, Counterfactual, Dream, Mutation, Consolidation.

Phase 2 Refactoring Insight:
  Current: Sleep does everything in one shot
  Future: Break into stages with ReplayScheduler (async)
  
  ReplayScheduler -> Episode Sampling -> Replay -> Sleep -> Consolidate
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from bio_agent_v4.interfaces.shared import PredictionError


class SleepEngine(ABC):
    """
    Consolidation: Replay, Counterfactual, Dream, Mutation, Consolidate.
    
    Input:  N recent episodes (from Episodic memory) + gene snapshot
    Output: Mutation proposals for Genome + semantic summary
    State:  Replay buffer, consolidation flags
    Clock:  Low-frequency tier (e.g., "sleep" when melatonin_high)
    
    Events:
        emit:   "sleep_consolidation_done" {mutations, summary}
        listen: "melatonin_high" (or time-based trigger)
    
    Latency: ~1-10 ms per consolidation cycle (typically async, low priority)
    
    Pipeline (Phase 2):
      1. Replay        : Sample N episodes, replay logic
      2. Counterfactual: "What if I had answered differently?" (simulate via Prediction)
      3. Dream         : Combine 2-3 distant episodes for new patterns
      4. Mutation      : Propose Gene.base_rate updates
      5. Consolidate   : Write Semantic memory, flush storage
    """

    @abstractmethod
    def replay(self, n: int = 10) -> List[Dict]:
        """
        Sample recent episodes for replay.
        
        Args:
            n: How many episodes to sample
        
        Returns:
            List of episode dicts {input, response, outcome, emotion, pe, ...}
        """
        ...

    @abstractmethod
    def counterfactual_replay(self, episode: Dict, alternative_response: str) -> PredictionError:
        """
        Simulate: "If I had said X instead, what PE would result?"
        
        Does NOT call LLM (expensive). Uses PredictionEngine to mock outcome.
        
        Args:
            episode: Original episode
            alternative_response: What-if response
        
        Returns:
            Estimated PredictionError for the alternative
        """
        ...

    @abstractmethod
    def dream(self, episodes: List[Dict], k: int = 3) -> List[str]:
        """
        Combine k distant episodes, extract new insights.
        
        Example: Episode1 (Python learning) + Episode3 (Rust discovery) + Episode5 (optimization):
        -> Insight: "User's interest in languages correlates with performance exploration"
        
        Args:
            episodes: Candidate episodes
            k: How many to combine per dream
        
        Returns:
            List of insight strings (for potential Gene updates)
        """
        ...

    @abstractmethod
    def propose_mutations(self, counterfactual_results: List[PredictionError],
                          dreams: List[str]) -> Dict[str, float]:
        """
        Generate Gene mutation proposals.
        
        Based on counterfactual analysis + dream insights.
        
        Args:
            counterfactual_results: PE estimates for alternatives
            dreams: Discovered patterns
        
        Returns:
            {gene_name: suggested_delta_base_rate}
            e.g., {'gene_curiosity_boost': +0.1, 'gene_caution_trigger': -0.05}
        """
        ...

    @abstractmethod
    def consolidate(self) -> None:
        """
        Finalize consolidation: write Semantic memory, flush storage.
        
        Called after all replay/dream/mutation stages complete.
        """
        ...

    @abstractmethod
    def is_consolidation_time(self) -> bool:
        """
        Check if consolidation should run (e.g., melatonin high, low activity).
        
        Returns:
            True if consolidation should proceed
        """
        ...

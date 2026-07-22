"""
Attention Engines: Bottom-up (cheap) and Top-down (refined).

Bottle-neck: Input filtering to prevent world model saturation.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional
from bio_agent_v4.interfaces.shared import AttentionScore, RefinedAttentionScore


class CheapAttentionEngine(ABC):
    """
    Bottleneck 1: Fast input filtering (bottom-up, no goal context).
    
    Input:  Raw input text + recent buffer (~5-10 recent inputs)
    Output: List[AttentionScore] sorted by saliency, top-k passed to RefinedAttention
    State:  Rolling recency buffer (sensory memory, ~1KB)
    Clock:  Every turn (period 1)
    
    Events:
        emit:   "attention_cheap_done" {top_k_events, scores}
        listen: "input_received"
    
    Latency: ~0.1 ms
    """

    @abstractmethod
    def score(self, raw_input: str, recent_buffer: List[str]) -> AttentionScore:
        """
        Compute bottom-up salience for one input.
        
        Args:
            raw_input: Current user message
            recent_buffer: Last N inputs (for recency/repetition detection)
        
        Returns:
            AttentionScore with novelty, emotion_cue, recency, keyword_saliency
        """
        ...

    @abstractmethod
    def top_k(self, candidates: List[Tuple[str, AttentionScore]], k: int) -> List[str]:
        """
        Filter to top-k by total score.
        
        Args:
            candidates: List of (text, score) tuples
            k: How many to pass through
        
        Returns:
            List of top-k input texts
        """
        ...

    @abstractmethod
    def batch_score(self, inputs: List[str]) -> List[AttentionScore]:
        """
        Batch scoring for efficiency.
        
        Args:
            inputs: Multiple input texts
        
        Returns:
            Parallel list of AttentionScores
        """
        ...


class RefinedAttentionEngine(ABC):
    """
    Bottleneck 2: Goal-aware filtering (top-down, uses executive goal from t-1).
    
    Input:  Top-k inputs (from CheapAttention) + WorldModel snapshot + prior goal
    Output: RefinedAttentionScore per input, may trigger reread/clarify flags
    State:  None (stateless; reads WorldModel)
    Clock:  Every turn after WorldModel.update()
    
    Events:
        emit:   "attention_refined_done" {scores, needs_reread, needs_clarification}
        listen: "world_model_updated"
    
    Latency: ~0.1 ms
    """

    @abstractmethod
    def refine(self, world_snapshot: Dict, prior_goal: Optional[str],
               input_text: str) -> RefinedAttentionScore:
        """
        Apply top-down goal modulation.
        
        Args:
            world_snapshot: Output from WorldModel.snapshot()
            prior_goal: Goal selected in turn (t-1)
            input_text: The input to refine
        
        Returns:
            RefinedAttentionScore with goal_relevance, belief_conflict, surprise, etc.
        """
        ...

    @abstractmethod
    def detect_reread_trigger(self, score: RefinedAttentionScore) -> bool:
        """
        Should we re-read the input (e.g., it conflicts with current understanding)?
        
        Returns:
            True if needs_reread should be set
        """
        ...

    @abstractmethod
    def detect_clarify_trigger(self, score: RefinedAttentionScore) -> bool:
        """
        Should we ask for clarification (e.g., belief_conflict too high)?
        
        Returns:
            True if needs_clarification should be set
        """
        ...

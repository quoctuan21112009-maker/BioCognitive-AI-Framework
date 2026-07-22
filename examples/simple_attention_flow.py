"""
Example 1: Simple Attention Flow

Demonstrates:
  - CheapAttentionEngine scoring
  - RefinedAttentionEngine with goal context
  - How attention flows through the pipeline
"""

from bio_agent_v4.interfaces import (
    CheapAttentionEngine,
    RefinedAttentionEngine,
    AttentionScore,
    RefinedAttentionScore,
)
from typing import List, Tuple


class SimpleCheapAttention(CheapAttentionEngine):
    """Minimal implementation for demo."""

    def score(self, raw_input: str, recent_buffer: List[str]) -> AttentionScore:
        # Heuristic: novelty based on word count, emotion from exclamation marks
        novelty = min(len(raw_input) / 100, 1.0)  # Longer = more novel
        emotion_cue = 0.8 if "!" in raw_input else 0.3
        recency = 0.9 if raw_input not in recent_buffer else 0.5
        keyword_saliency = 0.7 if any(kw in raw_input.lower() for kw in ["help", "problem", "error"]) else 0.3

        total = (novelty + emotion_cue + recency + keyword_saliency) / 4

        return AttentionScore(
            novelty=novelty,
            emotion_cue=emotion_cue,
            recency=recency,
            keyword_saliency=keyword_saliency,
            total=total,
        )

    def top_k(self, candidates: List[Tuple[str, AttentionScore]], k: int) -> List[str]:
        sorted_candidates = sorted(candidates, key=lambda x: x[1].total, reverse=True)
        return [text for text, _ in sorted_candidates[:k]]

    def batch_score(self, inputs: List[str]) -> List[AttentionScore]:
        return [self.score(inp, []) for inp in inputs]


class SimpleRefinedAttention(RefinedAttentionEngine):
    """Goal-aware attention."""

    def refine(self, world_snapshot: dict, prior_goal: str, input_text: str) -> RefinedAttentionScore:
        goal_relevance = 0.9 if prior_goal and prior_goal.lower() in input_text.lower() else 0.3
        belief_conflict = 0.2  # Simplified
        prediction_surprise = 0.1  # Simplified
        importance = (goal_relevance + (1 - belief_conflict) + (1 - prediction_surprise)) / 3
        total = importance

        return RefinedAttentionScore(
            goal_relevance=goal_relevance,
            belief_conflict=belief_conflict,
            prediction_surprise=prediction_surprise,
            importance=importance,
            total=total,
            needs_reread=belief_conflict > 0.7,
            needs_clarification=prediction_surprise > 0.7,
        )

    def detect_reread_trigger(self, score: RefinedAttentionScore) -> bool:
        return score.needs_reread

    def detect_clarify_trigger(self, score: RefinedAttentionScore) -> bool:
        return score.needs_clarification


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXAMPLE 1: Simple Attention Flow")
    print("=" * 60)

    cheap_attn = SimpleCheapAttention()
    refined_attn = SimpleRefinedAttention()

    # Test inputs
    inputs = [
        "Hi there!",
        "I have a critical problem with my code.",
        "What time is it?",
        "Can you help me debug this error!",
    ]

    print("\n1. CHEAP ATTENTION (Bottom-up)")
    print("-" * 60)

    scores = []
    for inp in inputs:
        score = cheap_attn.score(inp, [])
        scores.append((inp, score))
        print(f"Input: '{inp}'")
        print(f"  Novelty: {score.novelty:.2f}")
        print(f"  Emotion: {score.emotion_cue:.2f}")
        print(f"  Recency: {score.recency:.2f}")
        print(f"  Saliency: {score.keyword_saliency:.2f}")
        print(f"  Total: {score.total:.2f}")
        print()

    # Get top 2
    top_2 = cheap_attn.top_k(scores, k=2)
    print(f"Top 2 inputs by cheap attention: {top_2}\n")

    print("\n2. REFINED ATTENTION (Top-down, with goal)")
    print("-" * 60)

    prior_goal = "debugging"
    print(f"Current goal: '{prior_goal}'\n")

    for inp in top_2:
        refined_score = refined_attn.refine({}, prior_goal, inp)
        print(f"Input: '{inp}'")
        print(f"  Goal relevance: {refined_score.goal_relevance:.2f}")
        print(f"  Belief conflict: {refined_score.belief_conflict:.2f}")
        print(f"  Prediction surprise: {refined_score.prediction_surprise:.2f}")
        print(f"  Importance: {refined_score.importance:.2f}")
        print(f"  Total: {refined_score.total:.2f}")
        print(f"  Needs reread: {refined_score.needs_reread}")
        print(f"  Needs clarification: {refined_score.needs_clarification}")
        print()

    print("\n" + "=" * 60)
    print("End Example 1")
    print("=" * 60)

"""
Example 3: Sleep Engine Consolidation

Demonstrates:
  - Episode replay
  - Counterfactual simulation (cheap, using prediction)
  - Dream generation (combining episodes)
  - Mutation proposal
  - Consolidation
"""

from bio_agent_v4.interfaces import PredictionError
from typing import List, Dict
import random


class SimpleSleepDemo:
    """Simulate sleep consolidation stages."""

    def __init__(self):
        # Simulate episodic memory
        self.episodes = [
            {
                "id": f"ep_{i}",
                "input": f"User question {i}",
                "response": f"AI response {i}",
                "outcome": "positive" if random.random() > 0.3 else "negative",
                "emotion": random.uniform(-1, 1),
                "pe": random.uniform(0, 0.5),
                "turn": i * 10,
            }
            for i in range(20)  # 20 recent episodes
        ]
        self.insights = []
        self.mutations = {}

    def replay(self, n: int = 5) -> List[Dict]:
        """Sample N episodes for replay."""
        sampled = random.sample(self.episodes, min(n, len(self.episodes)))
        print(f"  [Replay] Sampled {len(sampled)} episodes")
        for ep in sampled:
            print(f"    - {ep['id']}: {ep['input'][:30]}... (outcome={ep['outcome']})")
        return sampled

    def counterfactual_replay(
        self, episode: Dict, alternative_response: str
    ) -> PredictionError:
        """Simulate: 'What if I answered differently?'

        Uses Prediction engine (cheap), not LLM (expensive).
        """
        # Fake the computation: estimate PE for alternative
        actual_outcome = 1.0 if episode["outcome"] == "positive" else -1.0
        alt_outcome_sim = actual_outcome + random.uniform(-0.3, 0.3)  # Simulate

        error = PredictionError(
            sentiment=abs(0.5 - (alt_outcome_sim + 1) / 2),
            followup=random.uniform(0, 0.2),
            info=random.uniform(0, 0.1),
            goal=random.uniform(0, 0.15),
        )

        print(f"    - Counterfactual for {episode['id']}: PE={error.magnitude():.2f}")
        return error

    def dream(self, episodes: List[Dict], k: int = 3) -> List[str]:
        """Combine K distant episodes to extract insights."""
        if len(episodes) < k:
            return []

        combined = random.sample(episodes, k)
        print(f"  [Dream] Combining {k} episodes:")
        for ep in combined:
            print(f"    - {ep['id']} (turn {ep['turn']})")

        # Extract an insight
        insight = f"Pattern: Episodes with positive outcomes have avg PE {sum(e['pe'] for e in combined) / len(combined):.2f}"
        print(f"    Insight: {insight}")
        self.insights.append(insight)
        return [insight]

    def propose_mutations(self, counterfactual_results: List[PredictionError]) -> Dict[str, float]:
        """Propose Gene mutations based on analysis."""
        print(f"  [Mutation Proposal]")

        if counterfactual_results:
            avg_cf_pe = sum(e.magnitude() for e in counterfactual_results) / len(
                counterfactual_results
            )
            print(f"    Average counterfactual PE: {avg_cf_pe:.2f}")

            # Simple heuristic: if PE high, boost exploration
            mutations = {
                "gene_curiosity_boost": 0.1 if avg_cf_pe > 0.3 else -0.05,
                "gene_caution_trigger": 0.05 if avg_cf_pe > 0.4 else -0.1,
                "gene_memory_retention": 0.15,  # Always boost memory
            }
        else:
            mutations = {}

        for gene, delta in mutations.items():
            print(f"    {gene}: {delta:+.2f}")
        self.mutations.update(mutations)
        return mutations

    def consolidate(self) -> None:
        """Finalize consolidation: write semantic memory, flush storage."""
        print(f"  [Consolidation]")
        print(f"    Insights extracted: {len(self.insights)}")
        print(f"    Mutations proposed: {len(self.mutations)}")
        print(f"    Flushing storage...")


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 3: Sleep Engine Consolidation")
    print("=" * 70)
    print()
    print("Scenario: Agent has accumulated 20 episodes during the day.")
    print("Now it's sleep time (melatonin_high), consolidating experiences.")
    print()

    demo = SimpleSleepDemo()

    print("\nSTAGE 1: REPLAY")
    print("-" * 70)
    replayed = demo.replay(n=5)

    print("\nSTAGE 2: COUNTERFACTUAL REPLAY")
    print("-" * 70)
    print("Simulating alternatives (no LLM calls, using Prediction engine):")
    cf_results = []
    for ep in replayed[:3]:
        alt = f"Alternative response for {ep['id']}"
        error = demo.counterfactual_replay(ep, alt)
        cf_results.append(error)

    print("\nSTAGE 3: DREAM (Combine distant episodes)")
    print("-" * 70)
    dream_insights = demo.dream(replayed, k=3)

    print("\nSTAGE 4: MUTATION PROPOSAL")
    print("-" * 70)
    mutations = demo.propose_mutations(cf_results)

    print("\nSTAGE 5: CONSOLIDATE")
    print("-" * 70)
    demo.consolidate()

    print("\n" + "=" * 70)
    print("Sleep Consolidation Summary")
    print("=" * 70)
    print(f"Episodes analyzed: {len(replayed)}")
    print(f"Counterfactual simulations: {len(cf_results)}")
    print(f"Dream insights: {len(demo.insights)}")
    print(f"Gene mutations proposed: {len(mutations)}")
    print(f"\nMutations to be applied to Genome:")
    for gene, delta in mutations.items():
        print(f"  {gene}: {delta:+.3f}")
    print("=" * 70)

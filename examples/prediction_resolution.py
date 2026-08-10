"""
Example 2: Multi-turn Prediction Resolution

Demonstrates:
  - PredictionEngine making predictions
  - Pending predictions awaiting resolution
  - PredictionErrorEngine computing errors with attribution
  - UncertaintyEngine tracking stats
"""

from bio_agent_v4.interfaces import (
    PredictionResult,
    PredictionError,
    UncertaintyState,
)
import random


class SimplePredictionDemo:
    """Simulate multi-turn prediction & resolution."""

    def __init__(self):
        self.pending_predictions = {}  # prediction_id -> PredictionResult
        self.prediction_counter = 0
        self.errors = []
        self.uncertainty = UncertaintyState(
            mean_pe=0.0,
            variance_pe=0.0,
            trend_pe=0.0,
            mode="exploit",
            context="conversation",
            n_samples=0,
        )

    def make_prediction(self, turn: int) -> str:
        """Generate a prediction at turn N."""
        pred = PredictionResult(
            expected_sentiment=random.uniform(0, 1),
            expected_followup=random.uniform(0, 1),
            expected_confidence=random.uniform(0.5, 1),
            expected_goal_completion=random.uniform(0, 1),
            expected_information_gain=random.uniform(0, 1),
            uncertainty=random.uniform(0, 0.5),
            turn_made=turn,
            resolved=False,
        )
        pred_id = f"pred_{self.prediction_counter}"
        self.prediction_counter += 1
        self.pending_predictions[pred_id] = pred
        return pred_id

    def try_resolve(self, turn: int) -> list:
        """Check which predictions can resolve at turn N."""
        resolved = []

        for pred_id, pred in list(self.pending_predictions.items()):
            # Sentiment resolves immediately
            if pred.turn_made == turn and not pred.resolved:
                actual_sentiment = random.uniform(-1, 1)
                error_sentiment = abs(pred.expected_sentiment - (actual_sentiment + 1) / 2)

                # Compute error with attribution
                error = PredictionError(
                    sentiment=error_sentiment,
                    followup=0.0,  # Not resolved yet
                    info=0.0,
                    goal=0.0,
                    world_error=random.uniform(0, error_sentiment * 0.3),
                    planner_error=random.uniform(0, error_sentiment * 0.3),
                    prediction_error=random.uniform(0, error_sentiment * 0.4),
                    llm_error=random.uniform(0, error_sentiment * 0.3),
                )

                resolved.append((pred_id, pred, error))
                self.errors.append(error)

                # Update uncertainty
                self._update_uncertainty()

        return resolved

    def _update_uncertainty(self):
        """Compute rolling uncertainty stats."""
        if not self.errors:
            return

        recent_errors = self.errors[-10:]  # Last 10
        magnitudes = [e.magnitude() for e in recent_errors]

        mean = sum(magnitudes) / len(magnitudes)
        variance = sum((m - mean) ** 2 for m in magnitudes) / len(magnitudes)
        trend = (magnitudes[-1] - magnitudes[0]) if len(magnitudes) > 1 else 0

        self.uncertainty = UncertaintyState(
            mean_pe=mean,
            variance_pe=variance,
            trend_pe=trend,
            mode="explore" if variance > 0.1 and trend > 0 else "exploit",
            context="conversation",
            n_samples=len(self.errors),
        )


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 2: Multi-turn Prediction Resolution")
    print("=" * 70)

    demo = SimplePredictionDemo()

    print("\nSimulating 5 turns of conversation...\n")

    for turn in range(5):
        print(f"\n--- TURN {turn} ---")

        # Step 1: Make prediction
        pred_id = demo.make_prediction(turn)
        pred = demo.pending_predictions[pred_id]
        print(f"\nPrediction made: {pred_id}")
        print(f"  Expected sentiment: {pred.expected_sentiment:.2f}")
        print(f"  Expected followup: {pred.expected_followup:.2f}")
        print(f"  Expected confidence: {pred.expected_confidence:.2f}")
        print(f"  Expected goal completion: {pred.expected_goal_completion:.2f}")
        print(f"  Uncertainty: {pred.uncertainty:.2f}")
        print(f"  Status: pending")

        # Step 2: Try resolve previous predictions
        if turn > 0:
            resolved_list = demo.try_resolve(turn - 1)
            if resolved_list:
                print(f"\n  [Resolution] {len(resolved_list)} prediction(s) resolved:")
                for pred_id_res, pred_res, error in resolved_list:
                    print(f"    {pred_id_res}:")
                    print(f"      Sentiment error: {error.sentiment:.2f}")
                    print(f"      Attribution: world={error.world_error:.2f}, "
                          f"planner={error.planner_error:.2f}, "
                          f"pred={error.prediction_error:.2f}, "
                          f"llm={error.llm_error:.2f}")
                    print(f"      Primary culprit: {error.primary_culprit()}")

        # Step 3: Show current uncertainty
        print(f"\n  Current uncertainty state:")
        print(f"    Mean PE: {demo.uncertainty.mean_pe:.2f}")
        print(f"    Variance PE: {demo.uncertainty.variance_pe:.2f}")
        print(f"    Trend PE: {demo.uncertainty.trend_pe:.2f}")
        print(f"    Mode: {demo.uncertainty.mode}")
        print(f"    Samples: {demo.uncertainty.n_samples}")

    print(f"\n\n" + "=" * 70)
    print("Final Summary")
    print("=" * 70)
    print(f"Total predictions made: {demo.prediction_counter}")
    print(f"Total errors computed: {len(demo.errors)}")
    print(f"Final uncertainty mode: {demo.uncertainty.mode}")
    print(f"Mean PE: {demo.uncertainty.mean_pe:.2f}")
    print(f"Variance PE: {demo.uncertainty.variance_pe:.2f}")
    print("=" * 70)

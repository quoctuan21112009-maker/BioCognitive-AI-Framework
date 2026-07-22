# BioCognitive-AI Framework v4 Examples

This directory contains runnable examples demonstrating key v4 concepts.

## Examples

### 1. Simple Attention Flow (`simple_attention_flow.py`)

Demonstrates:
- CheapAttentionEngine: bottom-up salience scoring
- RefinedAttentionEngine: top-down goal-aware filtering
- How attention scores flow through the pipeline

```bash
python examples/simple_attention_flow.py
```

**Output:** Attention scores for test inputs, with and without goal context.

---

### 2. Prediction Resolution (`prediction_resolution.py`)

Demonstrates:
- Making predictions at each turn
- Pending predictions awaiting resolution
- Computing prediction errors with module attribution
- Tracking uncertainty over multiple turns

```bash
python examples/prediction_resolution.py
```

**Output:** Multi-turn prediction lifecycle, error attribution, uncertainty evolution.

---

### 3. Sleep Consolidation (`sleep_consolidation.py`)

Demonstrates:
- Replay: sampling episodes
- Counterfactual: simulating alternatives (via Prediction, not LLM)
- Dream: combining distant episodes for insights
- Mutation: proposing gene updates
- Consolidation: finalizing changes

```bash
python examples/sleep_consolidation.py
```

**Output:** Full sleep consolidation pipeline with mutation proposals.

---

## Running All Examples

```bash
python examples/simple_attention_flow.py
python examples/prediction_resolution.py
python examples/sleep_consolidation.py
```

Or use a test runner:

```bash
for f in examples/*.py; do echo "\n=== $f ==="  && python "$f"; done
```

---

## Notes

- Examples use **simplified** implementations for clarity
- Real implementations will include complex logic (NLP, learning models, etc.)
- Focus is on demonstrating **data flow** and **interface contracts**
- All examples use the interface ABCs (not concrete implementations)

---

*Last updated: 2026-07-22*

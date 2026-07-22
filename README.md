# README: BioCognitive-AI Framework v4

## What is This?

The **BioCognitive-AI Framework v4** is a cognitive architecture inspired by biological neuroscience.

Replaces the linear pipeline of v3 with an interconnected **cognitive graph** featuring:

- Multi-turn reasoning with error feedback loops
- Goal-aware attention and executive function
- Meta-cognitive self-correction (draft → critic → rewrite)
- Prediction-driven learning with credit assignment
- Temporal memory tracking belief evolution
- Asynchronous consolidation (sleep-like learning)

---

## Quick Links

- **[Architecture Overview](docs/v4_architecture.md)** — 11 design insights, Phase 1-3
- **[Decision Flow](docs/decision_flow.md)** — Turn-by-turn pipeline
- **[Glossary](docs/glossary.md)** — Terminology & patterns
- **[Interfaces](bio_agent_v4/interfaces/)** — All ABCs

---

## Key Innovations

1. **Cognitive Graph** (not linear pipeline)
2. **DecisionContext Bottleneck** (prevent Executive bloat)
3. **Temporal Beliefs** (track evolution, not overwrite)
4. **Credit Assignment** (decompose PE to guide learning)
5. **Staged Meta-Cognition** (targeted rewrite, not binary)
6. **Weighted Memory** (no zero-out when any component is 0)
7. **Cheap Counterfactuals** (Prediction engine, not LLM)
8. **Performance Target**: 0.7–1.5 ms cognition + optimize for correctness

---

## Architecture

### **Input → Budget Decision**

**FAST** (~1-2 ms): Simple inputs bypass most cognition
**MEDIUM** (~2-5 ms): Moderate complexity
**DEEP** (~100-200 ms): High uncertainty, full pipeline

---

## Phase Status

✅ **Phase 1: Interfaces Blueprint** (DONE)
- All data structures defined
- All ABC interfaces defined
- Contracts locked down

🔄 **Phase 2: Critical Refactorings** (IN PROGRESS)
1. DecisionContext bottleneck
2. WorldModel façade
3. Temporal beliefs
4. Credit assignment
5. Critic decomposition
6. Memory formula
7. Sleep staging

🚀 **Phase 3: Performance & Polish** (FUTURE)
- Event sourcing, optimization, v3 integration, testing

---

## Project Structure

```
.
├── bio_agent_v4/
│   ├── interfaces/              # Phase 1: All ABCs
│   │   ├── shared.py            # Data structures
│   │   ├── attention.py
│   │   ├── world_model.py
│   │   ├── prediction.py
│   │   ├── motivation.py
│   │   ├── executive.py
│   │   ├── budget.py
│   │   ├── meta_cognition.py
│   │   ├── memory.py
│   │   └── sleep.py
│   ├── implementations/         # Phase 2-3
│   └── tests/                   # Phase 3
├── docs/
│   ├── v4_architecture.md
│   ├── decision_flow.md
│   └── glossary.md
├── README.md
└── requirements.txt
```

---

## Usage Example

```python
from bio_agent_v4.interfaces import (
    CheapAttentionEngine,
    AttentionScore,
    PredictionError,
)

# Implement interface
class MyCheapAttention(CheapAttentionEngine):
    def score(self, raw_input, recent_buffer):
        # Your implementation
        ...

# Use throughout codebase
attention: CheapAttentionEngine = MyCheapAttention()
score = attention.score(input_text, buffer)
```

---

## Performance Targets

```
Cognition per turn:     0.7–1.5 ms
  - CheapAttention:     0.1 ms
  - WorldModel update:  0.2 ms
  - Prediction:         0.2 ms
  - ExecutiveController: 0.05 ms
  - Meta-Cognition:     0.1 ms
  - Memory:             0.05 ms
  - Sleep:              async

LLM (bottleneck):       20–3000 ms
Ratio: Cognition ≈ 1% of total (optimize for correctness, not speed)
```

---

## Contributing

Contributions welcome! Especially:

1. Phase 2 module implementations
2. Tests for interfaces
3. Examples & tutorials
4. Performance optimization

---

## v3 Compatibility

v4 is a **redesign** (not a port). v3 components (GRN, Genome, Epigenome) will integrate with v4 in Phase 3.

---

## References

- **Global Workspace Theory** (Baars 1988)
- **Hierarchical Reinforcement Learning** (Barto & Mahadevan 2003)
- **Temporal Difference Learning** (Sutton & Barto 2018)
- **Meta-Cognition** (Flavell 1979, Thórisson 2011)
- **Sleep & Consolidation** (Born & Wilhelm 2012)

---

## License

MIT

---

## Contact

**Email:** quoctuan21112009@gmail.com  
**Repo:** https://github.com/quoctuan21112009-maker/BioCognitive-AI-Framework  

---

*Last updated: 2026-07-22*  
*Status: Phase 1 ✅ | Phase 2 🔄 | Phase 3 🚀*

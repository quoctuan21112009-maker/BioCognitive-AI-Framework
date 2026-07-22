# v4 Glossary

## Core Concepts

### Attention
- **CheapAttention**: Bottom-up filtering (novelty + emotion + recency + keywords). Fast, no goal context.
- **RefinedAttention**: Top-down filtering using current goal. Goal-aware but slower.

### World Model
- **Entity Graph**: Entities & relations
- **Belief Store**: Propositions about world ("User likes Python")
- **TemporalBelief**: Belief + turn + timestamp (preserves history)
- **Intent Store**: User's goals
- **Decision State**: Ongoing choices ("Weighing A vs B")
- **Learning State**: Progress tracking

### Prediction
- **PredictionResult**: Multi-dimensional {sentiment, followup, confidence, goal, info_gain}
- **Pending Buffer**: Predictions awaiting resolution
- **PredictionError**: Actual error + attribution {world_error, planner_error, llm_error, ...}

### Motivation
- **Need Graph**: Nodes=needs, edges=inhibitions
- **Lateral Inhibition**: High Safety suppresses Curiosity
- **Dominant Need**: Highest-activation need after competition

### Executive Function
- **Goal Stack**: Stack for task switching
- **DecisionContext**: Minimal context (active_goal, dominant_need, uncertainty, candidates, world_focus, planning_depth, error_signal, conflicting_goals)
- **Planning Horizon**: How many steps ahead to plan

### Meta-Cognition
- **Draft**: Initial LLM response
- **Critic**: Evaluates for errors (fact, hallucination, reasoning gaps)
- **CritiqueReport**: Structured issues list
- **Rewrite**: Improved response addressing issues

### Memory
- **Episodic**: Individual experience traces
- **Semantic**: Generalized knowledge
- **Importance**: weighted_sum(emotion, novelty, PE, uncertainty, goal_relevance)

### Sleep
- **Replay**: Re-run episodes
- **Counterfactual**: "What if I answered differently?" (Prediction engine, not LLM)
- **Dream**: Combine distant episodes for patterns
- **Mutation**: Propose Gene updates
- **Consolidate**: Write to Semantic memory

### Uncertainty
- **Mean PE**: Average error
- **Variance PE**: Inconsistency
- **Trend PE**: Rising = degrading model
- **Explore Mode**: High variance + rising trend
- **Exploit Mode**: Low variance + low mean PE

### CognitiveBudget
- **FAST**: Simple inputs, skip most cognition
- **MEDIUM**: Moderate complexity, include world + prediction
- **DEEP**: Complex, full pipeline

### Global Workspace
- **WorkspaceObject**: Immutable (key, owner, version, timestamp, ttl, payload)
- **Event Sourcing**: No edits; append new versions

---

## Key Patterns

### Bottleneck Pattern
Multiple inputs → ONE slim interface → consumer. (E.g., all modules → DecisionContext → Executive)

### Façade Pattern
One interface hides multiple specialists. (E.g., WorldModel hides EntityGraph, BeliefStore, etc.)

### Event Sourcing
No edits; append with versioning. (Full audit trail, easier debugging)

### Staged Processing
Large task into smaller stages. (E.g., Sleep: Replay → CF → Dream → Mutation → Consolidate)

---

## Abbreviations

- **PE**: Prediction Error
- **LLM**: Large Language Model
- **ABC**: Abstract Base Class (Python interface)
- **CF**: Counterfactual
- **GRN**: Gene Regulatory Network (v3)
- **Genome**: AI's genetic code (base_rates, updated via mutations)
- **Development**: Maturation stage (affects planning_horizon & mode)
- **Clock**: Periodic timer (hormone, trait, week tiers)
- **RMS**: Root mean square
- **TTL**: Time-to-live

---

## v3 → v4 Shifts

| v3 | v4 |
|----|----|
| Motivation scores | Need graph + inhibition |
| Single PE | Multi-dim PE + attribution |
| Binary critic pass | CritiqueReport + targeted rewrite |
| Product importance | Weighted sum |
| Flat goal | Goal stack |
| Instant prediction | Pending buffer + resolution latency |

---

*Last updated: 2026-07-22*

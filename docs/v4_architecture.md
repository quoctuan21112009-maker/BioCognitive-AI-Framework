# BioCognitive-AI Framework v4: Architecture & Migration

## Overview

The BioCognitive-AI Framework v4 is a complete redesign of the cognitive architecture from a **linear pipeline** to a **cognitive graph** inspired by biological neuroscience. This document explains the transition from v3 to v4 and the 11 key design insights.

---

## v3 → v4: The Fundamental Shift

### v3: Linear Pipeline
```
Input
  ↓
Trait (Gene-driven personality)
  ↓
Hormone (Neuromodulator state)
  ↓
Planner (Action planning)
  ↓
LLM (Text generation)
  ↓
Memory (Episode storage)
```

**Issues:**
- Sequential; no feedback loops
- Modules could not communicate mid-turn
- Learning only via Genome mutations
- Executive function underdeveloped

---

### v4: Cognitive Graph
```
          World Model
          ↑      ↓
Attention → Prediction
     ↓         ↓
Motivation ← PE
      ↓
Executive
      ↓
Planner
      ↓
Meta-Cognition
      ↓
Memory
      ↓
Sleep (Consolidation)
```

**Advantages:**
- Gated, interconnected: World Model ↔ Prediction ↔ Motivation → Executive
- Feedback loops: PE feeds Uncertainty feeds Motivation
- Multiple decision points per turn
- Built-in error monitoring & correction (Meta-Cognition)
- Asynchronous consolidation (Sleep)

---

## 11 Key Design Insights

### 1. **Cognitive Graph Architecture (Done)**
Replaced linear pipeline with interconnected graph. Key connections:
- **World Model ↔ Prediction**: Beliefs inform predictions; predictions guide world updates
- **Prediction Error → Uncertainty → Motivation**: PE drives exploration/exploitation trade-off
- **Motivation → Executive**: Need graph determines goal priority
- **Executive → Planner**: Refined goal sent to planner
- **Meta-Cognition → Memory**: Only final (vetted) responses stored

---

### 2. **DecisionContext Bottleneck (Phase 2)**

**Problem:** Executive was reading 6+ modules → "God Module" bloat

**Solution:** Introduce `DecisionContext` as single input

**Bottleneck Pattern:**
```
All other modules → BUILD DecisionContext → Executive (reads ONLY this)
```

**Benefit:** Dependency graph collapses; Executive implementation stays stable while other modules evolve.

---

### 3. **WorldModel Façade Pattern (Phase 2)**

**Problem:** WorldModel directly manages 6 distinct storage layers

**Solution:** WorldModel becomes façade; each layer has specialist

**Benefit:** Each specialist can optimize independently.

---

### 4. **Temporal Beliefs (Phase 2)**

**Problem:** Naive belief updates overwrite history

**Solution:** `TemporalBelief` tracks evolution (Python → Rust → Go)

**Benefit:** PredictionEngine can use trends for better forecasts.

---

### 5. **Credit Assignment in Prediction Error (Phase 2)**

**Problem:** PE is collapsed into single value → Genome doesn't know which module to update

**Solution:** Decompose error into component attributions

**Benefit:** Genome learns precisely which module needs improvement.

---

### 6-11. **See docs/v4_architecture.md for complete details**

---

## Implementation Phases

### **Phase 1: Interfaces Blueprint (Done)** ✅
- All data structures defined
- All ABC interfaces defined
- No implementation, just contracts

### **Phase 2: Critical Refactorings (In Progress)**
1. DecisionContext bottleneck
2. WorldModel façade
3. Temporal beliefs
4. Credit assignment
5. Critic decomposition
6. Memory formula
7. Sleep staging

### **Phase 3: Performance & Polish (Future)**
1. Event sourcing
2. Optimization
3. Integration with v3
4. Testing
5. Documentation

---

## Quick Reference

**Key Files:**
- `bio_agent_v4/interfaces/shared.py` - All data structures
- `bio_agent_v4/interfaces/attention.py` - Attention engines
- `bio_agent_v4/interfaces/world_model.py` - World model contract
- `bio_agent_v4/interfaces/prediction.py` - Prediction & error engines
- `docs/v4_architecture.md` - Full architecture guide
- `docs/decision_flow.md` - Turn-by-turn pipeline
- `docs/glossary.md` - Terminology

---

*Last updated: 2026-07-22*

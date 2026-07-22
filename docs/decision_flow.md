# v4 Decision Flow: Detailed Pipeline Walkthrough

## Turn-by-Turn Execution

This document traces the complete cognitive pipeline for a single turn.

---

## Turn N: Complete Flow

### **Step 1: Input Reception** (T+0 ms)
User message arrives → Event: "input_received"

### **Step 2: Budget Decision** (T+0.05 ms)
CognitiveBudgetManager decides: FAST | MEDIUM | DEEP

### **Step 3: Cheap Attention** (T+0.1 ms)
Bottom-up salience filtering: novelty + emotion + recency + keywords

### **Step 4: World Model Update** (T+0.3 ms)
Incremental updates to entities, relations, beliefs (temporal), intents, decisions, learning, emotions

### **Step 5: Refined Attention** (T+0.4 ms) [MEDIUM/DEEP]
Top-down filtering using current goal

### **Step 6: Prediction** (T+0.6 ms) [MEDIUM/DEEP]
Multi-dimensional prediction: sentiment, followup, confidence, goal, info_gain

### **Step 7: Resolve Previous Predictions** (T+0.7 ms)
Check which predictions from earlier turns can be resolved; compute prediction errors with attribution

### **Step 8: Uncertainty Update** (T+0.75 ms)
Rolling stats: mean PE, variance PE, trend → decide explore vs exploit

### **Step 9: Motivation Network** (T+0.8 ms) [MEDIUM/DEEP]
Lateral inhibition: needs compete; dominant need emerges

### **Step 10: Build DecisionContext** (T+0.85 ms) [MEDIUM/DEEP]
All modules collaborate to populate DecisionContext

### **Step 11: Executive Decision** (T+0.9 ms) [MEDIUM/DEEP]
Executive reads ONLY DecisionContext, decides goal & planning horizon

### **Step 12: Planner & LLM** (T+1.0 ms)
Plan execution → LLM generates draft response

### **Step 13: Meta-Cognition** (T+100 ms) [DEEP]
CriticEngine evaluates → CritiqueReport → MetaCognitionEngine optional rewrite

### **Step 14: Memory Encoding** (T+101 ms)
Compute importance (weighted sum) → encode final response

### **Step 15: User Receives Response** (T+101 ms)

### **[Async] Sleep Consolidation**
Replay, Counterfactual, Dream, Mutation, Consolidate

---

## Timing Summary

```
FAST path:              ~1-2 ms
MEDIUM path:            ~2-5 ms
DEEP path:              ~100-200 ms
LLM (bottleneck):       20-3000 ms
Sleep (async):          1-10 ms per cycle
```

---

## Event Bus Messages

| Event | Emitter | Use Case |
|-------|---------|----------|
| `input_received` | Input handler | Triggers CognitiveBudgetManager |
| `budget_decided` | CognitiveBudgetManager | Routes to FAST/MEDIUM/DEEP |
| `attention_cheap_done` | CheapAttention | Passes to RefinedAttention |
| `world_model_updated` | WorldModel | Triggers Prediction |
| `prediction_made` | PredictionEngine | Registers for resolution |
| `prediction_error_computed` | ErrorEngine | Updates Uncertainty |
| `uncertainty_updated` | UncertaintyEngine | Triggers Motivation |
| `motivation_updated` | MotivationNetwork | Triggers Executive |
| `executive_decision_made` | ExecutiveController | Triggers Planner |
| `response_finalized` | MetaCognition | Triggers Memory |
| `memory_encoded` | MemoryEncoder | Logged |
| `sleep_consolidation_done` | SleepEngine | Sent to Genome |

---

*Last updated: 2026-07-22*

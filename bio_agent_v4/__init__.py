"""
BioCognitive-AI Framework v4

A cognitive graph architecture inspired by biological neuroscience,
replacing the linear pipeline of v3 with a gated, interconnected system.

Key Components:
  - Attention: CheapAttention (bottom-up) + RefinedAttention (top-down)
  - WorldModel: Facade over Entity, Belief, Intent, Decision, Learning, Emotion stores
  - Prediction: Conversation + Self predictors with error decomposition
  - Motivation: Need graph with lateral inhibition
  - Executive: Goal selection, conflict resolution, planning horizon
  - CognitiveBudget: Routing (FAST/MEDIUM/DEEP)
  - MetaCognition: Draft → Critic → Rewrite → Choose
  - Memory: Weighted encoding with temporal tracking
  - Sleep: Replay, Counterfactual, Dream, Mutation, Consolidation

Version: 4.0.0
Architecture: Cognitive Graph
Target Latency: ~0.7-1.5 ms per cognition cycle (excluding LLM)
"""

__version__ = "4.0.0"
__author__ = "BioCognitive Team"

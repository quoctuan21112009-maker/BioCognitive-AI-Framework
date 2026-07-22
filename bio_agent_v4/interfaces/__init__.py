"""
Interfaces Package - Contract definitions for all v4 modules.

This package contains abstract base classes (ABCs) and dataclass contracts
for the entire v4 pipeline. Each module MUST implement its interface exactly,
so that refactoring individual modules does NOT break the rest of the system.

Organization:
  - shared.py         : Common data structures (AttentionScore, DecisionContext, etc.)
  - attention.py      : CheapAttentionEngine, RefinedAttentionEngine
  - world_model.py    : WorldModel facade
  - prediction.py     : PredictionEngine, PredictionErrorEngine, UncertaintyEngine
  - motivation.py     : MotivationNetwork (Need graph)
  - executive.py      : ExecutiveController
  - budget.py         : CognitiveBudgetManager
  - meta_cognition.py : CriticEngine, MetaCognitionEngine
  - memory.py         : MemoryEncoder
  - sleep.py          : SleepEngine
"""

from bio_agent_v4.interfaces.shared import (
    CognitiveBudget,
    AttentionScore,
    RefinedAttentionScore,
    Intent,
    Belief,
    DecisionState,
    LearningState,
    EmotionEstimate,
    PredictionResult,
    PredictionError,
    UncertaintyState,
    NeedState,
    ExecutiveDecision,
    MetaCognitionResult,
    DecisionContext,
    WorkspaceObject,
)

from bio_agent_v4.interfaces.attention import (
    CheapAttentionEngine,
    RefinedAttentionEngine,
)

from bio_agent_v4.interfaces.world_model import WorldModel
from bio_agent_v4.interfaces.prediction import (
    PredictionEngine,
    PredictionErrorEngine,
    UncertaintyEngine,
)
from bio_agent_v4.interfaces.motivation import MotivationNetwork
from bio_agent_v4.interfaces.executive import ExecutiveController
from bio_agent_v4.interfaces.budget import CognitiveBudgetManager
from bio_agent_v4.interfaces.meta_cognition import (
    CriticEngine,
    MetaCognitionEngine,
)
from bio_agent_v4.interfaces.memory import MemoryEncoder
from bio_agent_v4.interfaces.sleep import SleepEngine

__all__ = [
    # Enums & Data Classes
    "CognitiveBudget",
    "AttentionScore",
    "RefinedAttentionScore",
    "Intent",
    "Belief",
    "DecisionState",
    "LearningState",
    "EmotionEstimate",
    "PredictionResult",
    "PredictionError",
    "UncertaintyState",
    "NeedState",
    "ExecutiveDecision",
    "MetaCognitionResult",
    "DecisionContext",
    "WorkspaceObject",
    # Engines
    "CheapAttentionEngine",
    "RefinedAttentionEngine",
    "WorldModel",
    "PredictionEngine",
    "PredictionErrorEngine",
    "UncertaintyEngine",
    "MotivationNetwork",
    "ExecutiveController",
    "CognitiveBudgetManager",
    "CriticEngine",
    "MetaCognitionEngine",
    "MemoryEncoder",
    "SleepEngine",
]

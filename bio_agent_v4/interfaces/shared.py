"""
Shared Data Structures for v4 Pipeline

These dataclasses define the contracts between modules.
All fields are immutable-friendly (no mutable defaults except field(default_factory=...)).
"""

from abc import ABC
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime


# ============================================================
# ENUMS
# ============================================================

class CognitiveBudget(Enum):
    """Routing decision for computational resources."""
    FAST = "fast"       # Skip refined attention, world model write, prediction, meta
                        # Path: CheapAttention → Planner → LLM
    MEDIUM = "medium"  # Include attention + world model + prediction, skip meta/deep-sleep
                        # Path: Cheap/Refined Attention → World Model → Prediction → Planner → LLM
    DEEP = "deep"      # Full pipeline including meta-cognition and sleep consolidation
                        # Path: Full cognitive graph


# ============================================================
# ATTENTION
# ============================================================

@dataclass
class AttentionScore:
    """Output of CheapAttentionEngine for one input event.
    
    Bottom-up salience signals (no goal context yet).
    """
    novelty: float              # How new/unexpected [0..1]
    emotion_cue: float          # Emotional valence spike [0..1]
    recency: float              # How recently seen [-1..1]
    keyword_saliency: float     # Keyword/entity importance [0..1]
    total: float                # Weighted sum for ranking


@dataclass
class RefinedAttentionScore:
    """Output of RefinedAttentionEngine with goal context.
    
    Top-down modulation using executive goal from (t-1).
    """
    goal_relevance: float           # Relevance to current goal [0..1]
    belief_conflict: float          # Conflict with existing beliefs [0..1]
    prediction_surprise: float      # Violates model prediction [0..1]
    importance: float               # Overall priority [0..1]
    total: float                    # Final ranking score
    needs_reread: bool = False      # Trigger re-reading mechanism
    needs_clarification: bool = False  # Request user clarification


# ============================================================
# WORLD MODEL COMPONENTS
# ============================================================

@dataclass
class Intent:
    """User's expressed or inferred goal/intention."""
    text: str
    status: str = "active"          # active | fulfilled | abandoned
    confidence: float = 0.5
    created_turn: int = 0
    updated_turn: int = 0


@dataclass
class Belief:
    """Model of world state: 'subject predicate object'.
    
    Example: Belief(subject='User', predicate='likes', obj='Python', confidence=0.9)
    """
    subject: str
    predicate: str
    obj: str
    confidence: float
    last_updated_turn: int = 0


@dataclass
class TemporalBelief:
    """Belief with timestamp to track evolution.
    
    Replaces naive overwrite: 'User likes Python' (2009) → 'likes Rust' (2010) → 'likes Go' (2011)
    
    Enables prediction engines to use historical trend.
    """
    belief: Belief
    turn: int
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DecisionState:
    """Track ongoing user decision/reasoning.
    
    Example: User weighing option A vs B, leaning towards A but not committed.
    """
    subject: str                    # What is being decided
    options: List[str]              # Candidate choices
    leaning: Optional[str] = None   # Current preference
    resolved: bool = False          # Decision made


@dataclass
class LearningState:
    """Track user's learning progression on a topic.
    
    Does NOT overwrite; tracks stage transitions.
    Example: 'CNN' → learning (turn 0-10) → practicing (turn 11-20) → understood (turn 21+)
    """
    topic: str
    stage: str = "learning"         # learning | practicing | understood | mastered
    turns_active: int = 0           # How many turns at current stage
    confidence: float = 0.3         # Model's confidence in stage assessment


@dataclass
class EmotionEstimate:
    """Estimate of USER's emotional state (not agent's hormone).
    
    Used for memory importance weighting and conversation tone.
    """
    valence: float                  # Pleasantness: -1 (negative) .. +1 (positive)
    arousal: float                  # Intensity: 0 (calm) .. 1 (excited/stressed)
    label: Optional[str] = None     # Human-readable label: happy, confused, frustrated, etc.
    confidence: float = 0.5         # How sure are we about this estimate


# ============================================================
# PREDICTION
# ============================================================

@dataclass
class PredictionResult:
    """Multi-dimensional prediction output (not collapsed to single value).
    
    Each dimension has different resolution latency:
      - sentiment: resolves in same turn (immediate user reaction)
      - followup: resolves in 2-3 turns (does user continue on topic?)
      - confidence: used by meta-cognition immediately
      - goal_completion: resolves over multiple turns
      - information_gain: estimated from entropy reduction
    """
    expected_sentiment: float           # Predicted user satisfaction [-1..1]
    expected_followup: float            # Probability user continues on topic [0..1]
    expected_confidence: float          # AI's confidence in response [0..1]
    expected_goal_completion: float     # Probability current goal resolves [0..1]
    expected_information_gain: float    # Estimated entropy reduction [0..1]
    uncertainty: float                  # Overall epistemic uncertainty [0..1]
    turn_made: int = 0                  # Turn number when prediction made
    resolved: bool = False              # All dimensions resolved yet?

    def is_partially_resolved(self) -> bool:
        """Sentiment usually resolves before followup/goal."""
        return not self.resolved  # Override in implementation for dimension-specific logic


@dataclass
class PredictionError:
    """Credit assignment: which module made the error?
    
    Replaces collapsed PE with component breakdown for Genome learning.
    """
    sentiment: float                # Error in sentiment prediction
    followup: float                 # Error in followup prediction
    info: float                     # Error in information gain estimate
    goal: float                     # Error in goal completion estimate
    
    # (Optional) Attribution to modules
    world_error: float = 0.0        # World model inaccuracy
    planner_error: float = 0.0      # Planner failure
    memory_error: float = 0.0       # Memory/context confusion
    prediction_error: float = 0.0   # Predictor's own error
    llm_error: float = 0.0          # LLM generation failure

    def magnitude(self) -> float:
        """RMS of main dimensions."""
        return (abs(self.sentiment)**2 + abs(self.followup)**2 + 
                abs(self.info)**2 + abs(self.goal)**2) ** 0.5 / 2

    def primary_culprit(self) -> str:
        """Which module is mostly responsible?"""
        errors = {
            'world': self.world_error,
            'planner': self.planner_error,
            'memory': self.memory_error,
            'prediction': self.prediction_error,
            'llm': self.llm_error,
        }
        return max(errors, key=errors.get) if any(errors.values()) else 'unknown'


@dataclass
class UncertaintyState:
    """Rolling statistics on prediction errors.
    
    Used to decide explore vs exploit, and to trigger deeper cognition.
    """
    mean_pe: float                  # Average magnitude of recent PE
    variance_pe: float              # Variability in recent PE
    trend_pe: float                 # Is PE increasing (→ explore) or decreasing (→ exploit)?
    mode: str = "exploit"           # "explore" when variance high + trend rising
    context: str = "general"        # Belief, Goal, Conversation context
    n_samples: int = 0              # How many PE samples in history


# ============================================================
# MOTIVATION
# ============================================================

@dataclass
class NeedState:
    """One node in the Need graph (not a simple list of scores).
    
    Example: Safety, Curiosity, Affiliation, Achievement
    Needs inhibit each other through lateral inhibition.
    """
    name: str                       # Safety, Curiosity, Affiliation, etc.
    level: float                    # Current activation [0..1]
    inhibits: List[str] = field(default_factory=list)  # Which other needs this suppresses
    activated_by: List[str] = field(default_factory=list)  # Which drives boost this need
    last_satisfied_turn: int = 0    # When was this need last addressed?


# ============================================================
# EXECUTIVE
# ============================================================

@dataclass
class ExecutiveDecision:
    """Output of ExecutiveController.
    
    Bundles: goal selection, conflict resolution, inhibition, task switching,
    planning horizon, error monitoring, action sequencing.
    """
    selected_goal: str              # Primary goal to pursue
    conflicting_goals: List[str] = field(default_factory=list)  # Goals that lost
    inhibited_actions: List[str] = field(default_factory=list)  # Actions suppressed
    planning_horizon: int = 5       # How many steps to plan ahead
    mode: str = "direct"           # direct | reflective | creative (from Development stage)
    reason: str = ""               # Why this goal? (for debugging)


# ============================================================
# META-COGNITION
# ============================================================

@dataclass
class MetaCognitionResult:
    """Final response after draft → critic → (optional) rewrite."""
    draft: str                      # Initial response
    confidence: float               # Critic's confidence [0..1]
    need_rewrite: bool              # Did critic request rewrite?
    final_response: str             # After rewrites (or same as draft)
    rewrite_count: int = 0          # How many rewrites performed
    critique_issues: List[str] = field(default_factory=list)  # Issues found


# ============================================================
# CRITICAL: DecisionContext (Phase 2 Refactoring)
# ============================================================

@dataclass
class DecisionContext:
    """Minimal context for ExecutiveController to decide.
    
    Bottleneck to prevent "God Module" bloat.
    All other modules build this context; Executive only reads this.
    
    From design doc: this replaces Executive reading Need, WorldModel,
    Development, Uncertainty, Prediction, Emotion, Hormone, Trait.
    """
    active_goal: Optional[str]      # Current goal or None
    dominant_need: NeedState        # Current strongest need
    uncertainty: UncertaintyState   # Epistemic state
    candidate_actions: List[str] = field(default_factory=list)  # Top K options from Planner
    world_focus: Dict[str, Any] = field(default_factory=dict)  # Key entities/relations to track
    planning_depth: int = 5         # From Development stage
    error_signal: Optional[PredictionError] = None  # Recent error if any
    conflicting_goals: List[str] = field(default_factory=list)  # Alternative goals


# ============================================================
# PHASE 3: Event Sourcing & Immutability (Global Workspace)
# ============================================================

@dataclass
class WorkspaceObject:
    """Immutable object in Global Workspace (event sourcing pattern).
    
    No one edits old versions. Always append new version.
    Simulates immutable memory + version control.
    """
    key: str                        # Identifier (e.g., 'goal_stack', 'emotion')
    owner: str                      # Which module owns this (e.g., 'ExecutiveController')
    version: int                    # Version number (auto-increment)
    timestamp: datetime = field(default_factory=datetime.now)  # When created
    ttl: Optional[float] = None     # Time-to-live in seconds (None = persistent)
    payload: Dict[str, Any] = field(default_factory=dict)  # Actual data

    def is_expired(self) -> bool:
        """Check if TTL exceeded."""
        if self.ttl is None:
            return False
        age = (datetime.now() - self.timestamp).total_seconds()
        return age > self.ttl


# ============================================================
# MEMORY & CONSOLIDATION
# ============================================================

@dataclass
class MemoryImportanceWeights:
    """Components for memory importance formula (Phase 2 refactoring).
    
    Instead of: importance = emotion × novelty × PE × uncertainty (product)
    Use: importance = w1*emotion + w2*novelty + w3*PE + w4*uncertainty + w5*goal_relevance
    
    Avoids zero-out when any component is 0.
    """
    w_emotion: float = 0.25
    w_novelty: float = 0.25
    w_pe: float = 0.25
    w_uncertainty: float = 0.15
    w_goal_relevance: float = 0.10

    def compute(self, emotion: float, novelty: float, pe: float,
                 uncertainty: float, goal_relevance: float) -> float:
        """Linear weighted sum [0..1]."""
        total = (self.w_emotion * emotion +
                 self.w_novelty * novelty +
                 self.w_pe * pe +
                 self.w_uncertainty * uncertainty +
                 self.w_goal_relevance * goal_relevance)
        return min(1.0, max(0.0, total))  # Clamp to [0..1]

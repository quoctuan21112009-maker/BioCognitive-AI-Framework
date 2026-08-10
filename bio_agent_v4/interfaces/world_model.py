"""
World Model: Facade over distributed stores.

Phase 2 Refactoring Insight:
  Current: WorldModel reads/writes 6 different storage layers directly
  Future: WorldModel becomes facade, delegating to specialists
  
  WorldModel
    ├── EntityGraph (entities + relations)
    ├── BeliefStore (with TemporalBelief tracking)
    ├── IntentStore (user goals)
    ├── DecisionStore (ongoing decision states)
    ├── LearningStore (learning progressions)
    └── EmotionStore (emotional estimates)
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from bio_agent_v4.interfaces.shared import (
    Intent,
    Belief,
    TemporalBelief,
    DecisionState,
    LearningState,
    EmotionEstimate,
)


class WorldModel(ABC):
    """
    Cognitive map: entities, relations, beliefs, intents, decisions, learning.
    
    Input:  Filtered input (after CheapAttention), current turn number
    Output: snapshot() -> comprehensive dict, or specialized query()
    State:  Persistent, incremental updates (no full rebuild per turn)
    Clock:  Every turn (period 1, lightweight)
    
    Events:
        emit:   "world_model_updated" {snapshot, changed_keys}
        listen: "attention_cheap_done"
    
    Latency: ~0.2 ms (incremental, not full recompute)
    
    Critical Design (Phase 2):
      - No module outside WorldModel directly accesses stored beliefs/intents
      - All queries go through query() or snapshot()
      - Conflict resolution happens inside resolve_conflicts() before returning
      - Temporal beliefs prevent naive overwrite (tracks belief evolution)
    """

    # ---- Entity & Relation Layer ----

    @abstractmethod
    def update_entities(self, extracted_entities: Dict[str, Any]) -> None:
        """
        Add/update entities mentioned in current input.
        
        Args:
            extracted_entities: {entity_id: {name, type, properties, ...}}
        """
        ...

    @abstractmethod
    def update_relations(self, extracted_relations: List[Tuple[str, str, str]]) -> None:
        """
        Add/update relations (entity1, relation_type, entity2).
        
        Args:
            extracted_relations: List of (subject, predicate, object)
        """
        ...

    @abstractmethod
    def query_entities(self, entity_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve entity or all entities.
        
        Args:
            entity_id: Specific entity to query, or None for all
        
        Returns:
            Entity data or dict of all entities
        """
        ...

    @abstractmethod
    def query_relations(self, subject: Optional[str] = None) -> List[Tuple[str, str, str]]:
        """
        Retrieve relations, optionally filtered by subject.
        
        Args:
            subject: Filter by subject, or None for all
        
        Returns:
            List of (subject, predicate, object) tuples
        """
        ...

    # ---- Belief Layer (with Temporal Tracking) ----

    @abstractmethod
    def update_beliefs(self, new_evidence: List[Belief], turn: int) -> None:
        """
        Add/update beliefs from current input.
        
        IMPORTANT: Uses TemporalBelief internally to track evolution.
        Does NOT simply overwrite 'User likes X'; instead records:
          Python (turn 0) -> Rust (turn 100) -> Go (turn 200)
        
        Args:
            new_evidence: List of new Belief objects
            turn: Current turn number
        """
        ...

    @abstractmethod
    def query_beliefs(self, subject: Optional[str] = None,
                      predicate: Optional[str] = None,
                      include_history: bool = False) -> List[Belief]:
        """
        Query current beliefs, optionally with full temporal history.
        
        Args:
            subject: Filter by subject
            predicate: Filter by relation type
            include_history: Return TemporalBeliefs with full history?
        
        Returns:
            List of Belief objects (or TemporalBelief if include_history)
        """
        ...

    @abstractmethod
    def get_belief_trend(self, subject: str, predicate: str) -> List[TemporalBelief]:
        """
        Get historical evolution of a specific belief.
        
        Used by PredictionEngine to leverage trends (e.g., user's interests drifting).
        
        Args:
            subject: Subject entity
            predicate: Relation type
        
        Returns:
            Ordered list of TemporalBelief from oldest to newest
        """
        ...

    # ---- Intent Layer ----

    @abstractmethod
    def update_intents(self, extracted_intents: List[str], turn: int) -> None:
        """
        Add/update user intents from current input.
        
        Args:
            extracted_intents: List of intent descriptions
            turn: Current turn
        """
        ...

    @abstractmethod
    def query_active_intents(self) -> List[Intent]:
        """
        Get all currently active intents (status='active').
        
        Returns:
            List of Intent objects
        """
        ...

    # ---- Decision State Layer ----

    @abstractmethod
    def update_decision_state(self, subject: str, options: List[str],
                              leaning: Optional[str] = None) -> None:
        """
        Track ongoing decision (user weighing options).
        
        Args:
            subject: What is being decided
            options: Candidate choices
            leaning: Current preference (optional)
        """
        ...

    @abstractmethod
    def resolve_decision(self, subject: str, choice: str) -> None:
        """
        Mark a decision as resolved.
        
        Args:
            subject: Which decision
            choice: The choice made
        """
        ...

    @abstractmethod
    def query_decision_states(self) -> List[DecisionState]:
        """
        Get all ongoing decisions.
        
        Returns:
            List of DecisionState objects
        """
        ...

    # ---- Learning State Layer ----

    @abstractmethod
    def update_learning_state(self, topic: str, signal: str, turn: int) -> None:
        """
        Track learning progression on a topic.
        
        Args:
            topic: What is being learned
            signal: Signal about progress (e.g., 'correct_answer', 'confused', 'mastered')
            turn: Current turn
        """
        ...

    @abstractmethod
    def query_learning_states(self) -> List[LearningState]:
        """
        Get all active learning states.
        
        Returns:
            List of LearningState objects
        """
        ...

    # ---- Emotion Layer ----

    @abstractmethod
    def update_emotion_estimate(self, text: str, turn: int) -> EmotionEstimate:
        """
        Estimate user's emotional state from current input.
        
        Args:
            text: The user message
            turn: Current turn
        
        Returns:
            EmotionEstimate (valence, arousal, label)
        """
        ...

    @abstractmethod
    def query_emotion_history(self, window: int = 5) -> List[EmotionEstimate]:
        """
        Get recent emotion estimates.
        
        Args:
            window: How many recent turns to include
        
        Returns:
            List of EmotionEstimate, most recent last
        """
        ...

    # ---- Conflict Resolution ----

    @abstractmethod
    def resolve_conflicts(self) -> List[str]:
        """
        Detect and resolve contradictions in world model.
        
        Examples:
          - DecisionState says "deciding A vs B" but Belief says "chose A" -> resolve
          - LearningState says "confused" but recent positive feedback -> update
          - Beliefs conflict (User likes Python AND User hates Python) -> trust recency
        
        Returns:
            List of conflict descriptions (for logging/debugging)
        """
        ...

    # ---- Snapshot & Query ----

    @abstractmethod
    def snapshot(self) -> Dict[str, Any]:
        """
        Comprehensive snapshot of world model state.
        
        Returns dict with keys:
          - entities: {entity_id: {...}}
          - relations: [(subject, pred, obj), ...]
          - beliefs: [Belief, ...]
          - intents: [Intent, ...]
          - decisions: [DecisionState, ...]
          - learning: [LearningState, ...]
          - emotions: [EmotionEstimate, ...]
          - conflicts_resolved: [str, ...]
          - timestamp: datetime
        
        Returns:
            Dict representation of complete world model
        """
        ...

    @abstractmethod
    def query(self, query_type: str, **kwargs) -> Any:
        """
        Generic query interface for extensibility.
        
        Args:
            query_type: Type of query ('entity', 'belief', 'intent', etc.)
            **kwargs: Query parameters
        
        Returns:
            Query result
        """
        ...

    @abstractmethod
    def clear_turn_transient(self) -> None:
        """
        Clear turn-specific transient state (not persistent beliefs/intents).
        
        Called at turn boundary to avoid stale data.
        """
        ...

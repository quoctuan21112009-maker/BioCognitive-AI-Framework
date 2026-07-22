# Contributing to BioCognitive-AI Framework v4

Thank you for your interest in contributing! Here's how to get started.

---

## Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/BioCognitive-AI-Framework.git
   cd BioCognitive-AI-Framework
   ```
3. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Install dev dependencies**:
   ```bash
   make install-dev
   ```

---

## Development Workflow

### Code Quality

Before committing, run:

```bash
make format  # Black + isort
make lint    # Flake8 + pylint
make type-check  # mypy
```

Or use the pre-commit hook:

```bash
pip install pre-commit
pre-commit install
```

### Testing

```bash
make test  # Run tests
make coverage  # Run tests + coverage report
```

### Examples

```bash
make run-examples  # Run all examples
```

---

## Contributing Areas

Priority areas for Phase 2-3:

### Phase 2: Critical Refactorings
1. **DecisionContext Bottleneck**
   - Refactor ExecutiveController to read ONLY DecisionContext
   - Implement DecisionContext builder in other modules
   - File: `bio_agent_v4/implementations/executive_impl.py`

2. **WorldModel Façade**
   - Split WorldModel into specialist stores
   - File: `bio_agent_v4/implementations/world_model_impl.py`

3. **Temporal Beliefs**
   - Implement TemporalBelief tracking
   - File: `bio_agent_v4/implementations/world_model_impl.py`

4. **Credit Assignment**
   - Decompose PredictionError into components
   - File: `bio_agent_v4/implementations/prediction_impl.py`

5. **Critic Decomposition**
   - Implement CritiqueReport structure
   - File: `bio_agent_v4/implementations/meta_cognition_impl.py`

6. **Memory Formula**
   - Switch to weighted sum
   - File: `bio_agent_v4/implementations/memory_impl.py`

7. **Sleep Staging**
   - Implement Replay → CF → Dream → Mutation → Consolidate
   - File: `bio_agent_v4/implementations/sleep_impl.py`

### Phase 3: Performance & Polish
1. **Event Sourcing** - WorkspaceObject versioning
2. **Optimization** - Profile & target 0.7-1.5 ms
3. **Integration** - Connect v3 GRN/Genome/Epigenome
4. **Testing** - Comprehensive unit/integration/stress tests
5. **Documentation** - API reference, tutorials, case studies

---

## Commit Message Format

Use conventional commits:

```
type(scope): description

Optional body:
- Explain why
- Explain what changed
- Link to issues

type: feat|fix|refactor|test|docs|chore
scope: which module (attention, world-model, prediction, etc.)
```

Examples:
```
feat(executive): implement DecisionContext bottleneck
fix(prediction): resolve pending predictions correctly
test(sleep): add consolidation tests
docs(glossary): clarify lateral inhibition
```

---

## Pull Request Process

1. **Update** README.md with any new features
2. **Add tests** for new functionality
3. **Run** `make lint`, `make type-check`, `make test`
4. **Write** clear PR description
5. **Link** related issues
6. **Wait** for review & feedback

---

## Code Style

- **Black** for formatting (100-char line length)
- **isort** for import sorting
- **Type hints** for all public functions
- **Docstrings** for all classes & methods (Google style)

Example:

```python
from typing import Optional, List
from bio_agent_v4.interfaces import AttentionScore

class MyAttention:
    """Example attention engine.
    
    Attributes:
        buffer_size: Size of recent input buffer
    """
    
    def __init__(self, buffer_size: int = 10) -> None:
        """Initialize attention engine.
        
        Args:
            buffer_size: How many recent inputs to track
        """
        self.buffer_size = buffer_size
    
    def score(self, raw_input: str, recent_buffer: List[str]) -> AttentionScore:
        """Compute attention score.
        
        Args:
            raw_input: Current input
            recent_buffer: Recent inputs for context
        
        Returns:
            AttentionScore with salience components
        
        Raises:
            ValueError: If input is empty
        """
        if not raw_input:
            raise ValueError("Input cannot be empty")
        ...
```

---

## Reporting Bugs

Use GitHub Issues with template:

```
## Description
Clear, concise description

## Reproduction
1. Step 1
2. Step 2
3. ...

## Expected behavior
What should happen

## Actual behavior
What actually happens

## Environment
- OS: [Windows/Mac/Linux]
- Python: [3.10/3.11/...]
- Branch: [main/feature-x]
```

---

## Discussions

For design discussions or questions:
- **Discussions tab**: Use for debates, ideas, proposals
- **Issues**: Use for bugs, feature requests, tasks
- **Pull Requests**: Use for implementations

---

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors graph

---

## Questions?

Open an issue or start a discussion. We're happy to help!

---

*Last updated: 2026-07-22*

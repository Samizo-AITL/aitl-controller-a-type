# src/core/base.py

class ControllerBase:
    """Base class for all controllers."""

    def __init__(self, name: str = "controller"):
        self.name = name

    def reset(self):
        """Reset internal states (override in subclasses)."""
        pass

    def step(self, observation, t=None):
        """Compute control command (override in subclasses)."""
        raise NotImplementedError

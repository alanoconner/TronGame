"""Domain primitives for describing player direction."""
from __future__ import annotations

from enum import Enum


class Direction(str, Enum):
    """Represents the four cardinal directions a player can move."""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @property
    def vector(self) -> tuple[int, int]:
        """Return the unit vector for the direction."""
        if self is Direction.UP:
            return (0, -1)
        if self is Direction.DOWN:
            return (0, 1)
        if self is Direction.LEFT:
            return (-1, 0)
        return (1, 0)

    def opposite(self) -> "Direction":
        """Return the direction opposite to the current one."""
        match self:
            case Direction.UP:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.UP
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.LEFT

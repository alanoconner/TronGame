"""Player entity definitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from .direction import Direction

Color = Tuple[int, int, int]


@dataclass(slots=True)
class Player:
    """Represents a light cycle rider in the Tron game."""

    name: str
    position: tuple[float, float]  # Stored as the centre position.
    color: Color
    width: int
    direction: Direction
    speed: float
    trail_points: list[tuple[float, float]] = field(default_factory=list)

    def move(self) -> None:
        """Advance the player one step in the current direction."""
        dx, dy = self.direction.vector
        x, y = self.position
        self.position = (round(x + dx * self.speed, 1), round(y + dy * self.speed, 1))
        self.trail_points.append(self.position)

    def start_new_segment(self) -> None:
        """Record the beginning of a new trail segment."""
        self.trail_points.append(self.position)

    @property
    def radius(self) -> float:
        """Half of the player's width, useful for calculations."""
        return self.width / 2

    def as_rect(self) -> tuple[float, float, int, int]:
        """Return a rectangle describing the player's body for drawing."""
        x, y = self.position
        top_left = (x - self.radius, y - self.radius)
        return (*top_left, self.width, self.width)

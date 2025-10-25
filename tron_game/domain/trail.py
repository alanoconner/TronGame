"""Trail entity for storing a player's path."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(slots=True)
class Trail:
    """Collection of points forming a continuous trail."""

    max_length: int
    width: int
    points: list[tuple[float, float]] = field(default_factory=list)

    def add_point(self, point: tuple[float, float]) -> None:
        """Append a point and enforce the maximum length."""
        self.points.append(point)
        if len(self.points) > self.max_length:
            self.points.pop(0)

    def last_point(self) -> tuple[float, float]:
        """Return the most recently added point."""
        return self.points[-1]

    def segments(self) -> Iterable[tuple[tuple[float, float], tuple[float, float]]]:
        """Iterate over pairs of points representing consecutive segments."""
        for start, end in zip(self.points, self.points[1:]):
            yield start, end

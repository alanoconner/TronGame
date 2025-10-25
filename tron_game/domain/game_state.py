"""Aggregate root representing the state of a match."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .player import Player
from .trail import Trail


@dataclass(slots=True)
class GameState:
    """Mutable game state shared across application services."""

    player_one: Player
    player_two: Player
    trail_one: Trail
    trail_two: Trail
    running: bool = True
    winner: Optional[Player] = None

    def reset(self) -> None:
        """Reset the game state while preserving player identities."""
        self.player_one.trail_points.clear()
        self.player_two.trail_points.clear()
        self.trail_one.points.clear()
        self.trail_two.points.clear()
        self.running = True
        self.winner = None

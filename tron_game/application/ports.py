"""Application-level ports for dependency inversion."""
from __future__ import annotations

from typing import Optional, Protocol, Tuple

from tron_game.domain.player import Player
from tron_game.domain.trail import Trail

Color = Tuple[int, int, int]


class DisplayPort(Protocol):
    """Describes the operations required for rendering the game."""

    background_color: Color

    def clear(self) -> None:
        """Clear the drawing surface."""

    def draw_player(self, player: Player) -> None:
        """Render the player's light cycle."""

    def draw_trail(self, player: Player, trail: Trail) -> None:
        """Render a trail using the player's colour."""

    def draw_game_over(self, winner: Optional[Player]) -> None:
        """Render the game over overlay."""

    def update(self) -> None:
        """Flip the buffers to show the new frame."""

    def sample_color(self, position: tuple[int, int]) -> Color:
        """Return the colour at the given screen position."""

    def close(self) -> None:
        """Release any resources used by the display."""


class ClockPort(Protocol):
    """A thin abstraction for timing control."""

    def tick(self, frame_rate: int) -> None:
        """Block to maintain a constant frame rate."""

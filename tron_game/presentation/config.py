"""Configuration values for the presentation layer."""
from __future__ import annotations

from dataclasses import dataclass

from tron_game.domain.direction import Direction


@dataclass(frozen=True)
class PlayerConfig:
    name: str
    start_position: tuple[float, float]
    color: tuple[int, int, int]
    width: int
    direction: Direction
    speed: float


@dataclass(frozen=True)
class GameConfig:
    window_size: tuple[int, int] = (1024, 720)
    trail_width: int = 5
    trail_max_length: int = 1000
    background_color: tuple[int, int, int] = (0, 0, 0)
    frame_rate: int = 120
    player_one: PlayerConfig = PlayerConfig(
        name="Green Rider",
        start_position=(256, 360),
        color=(0, 255, 0),
        width=10,
        direction=Direction.UP,
        speed=0.3,
    )
    player_two: PlayerConfig = PlayerConfig(
        name="Red Rider",
        start_position=(768, 360),
        color=(255, 0, 0),
        width=10,
        direction=Direction.UP,
        speed=0.3,
    )

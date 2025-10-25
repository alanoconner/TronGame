"""Presentation layer orchestrating the pygame event loop."""
from __future__ import annotations

from collections import deque
from typing import Deque, Iterable

import pygame

from tron_game.application.game_service import GameService
from tron_game.domain.direction import Direction
from tron_game.domain.game_state import GameState
from tron_game.domain.player import Player
from tron_game.domain.trail import Trail
from tron_game.infrastructure.pygame_display import PygameClock, PygameDisplay
from .config import GameConfig


class InputHandler:
    """Converts pressed keys into direction changes."""

    def __init__(self) -> None:
        self._player_one_queue: Deque[Direction] = deque()
        self._player_two_queue: Deque[Direction] = deque()

    def record(self, keys: Iterable[int]) -> None:
        """Record pressed keys so they can be replayed sequentially."""
        if pygame.K_w in keys:
            self._player_one_queue.append(Direction.UP)
        if pygame.K_s in keys:
            self._player_one_queue.append(Direction.DOWN)
        if pygame.K_a in keys:
            self._player_one_queue.append(Direction.LEFT)
        if pygame.K_d in keys:
            self._player_one_queue.append(Direction.RIGHT)

        if pygame.K_UP in keys:
            self._player_two_queue.append(Direction.UP)
        if pygame.K_DOWN in keys:
            self._player_two_queue.append(Direction.DOWN)
        if pygame.K_LEFT in keys:
            self._player_two_queue.append(Direction.LEFT)
        if pygame.K_RIGHT in keys:
            self._player_two_queue.append(Direction.RIGHT)

    def consume_player_one(self) -> Iterable[Direction]:
        """Yield queued direction changes for player one."""
        yield from self._consume(self._player_one_queue)

    def consume_player_two(self) -> Iterable[Direction]:
        """Yield queued direction changes for player two."""
        yield from self._consume(self._player_two_queue)

    @staticmethod
    def _consume(queue: Deque[Direction]) -> Iterable[Direction]:
        """Consume an entire queue of recorded directions."""
        while queue:
            yield queue.popleft()


def build_game_state(config: GameConfig) -> GameState:
    """Create the domain objects that represent a fresh game state."""
    player_one = Player(
        name=config.player_one.name,
        position=config.player_one.start_position,
        color=config.player_one.color,
        width=config.player_one.width,
        direction=config.player_one.direction,
        speed=config.player_one.speed,
    )
    player_two = Player(
        name=config.player_two.name,
        position=config.player_two.start_position,
        color=config.player_two.color,
        width=config.player_two.width,
        direction=config.player_two.direction,
        speed=config.player_two.speed,
    )

    player_one.start_new_segment()
    player_two.start_new_segment()

    trail_one = Trail(max_length=config.trail_max_length, width=config.trail_width)
    trail_two = Trail(max_length=config.trail_max_length, width=config.trail_width)
    trail_one.add_point(player_one.position)
    trail_two.add_point(player_two.position)

    return GameState(player_one=player_one, player_two=player_two, trail_one=trail_one, trail_two=trail_two)


def run() -> None:
    """Entry point that configures dependencies and runs the game loop."""
    config = GameConfig()
    display = PygameDisplay(window_size=config.window_size, background_color=config.background_color)
    clock = PygameClock()
    state = build_game_state(config)
    service = GameService(state, display, config.window_size)
    input_handler = InputHandler()

    running = True
    while running:
        pressed_keys: list[int] = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    state.running = False
                    break
                pressed_keys.append(event.key)

        if not running:
            continue

        input_handler.record(pressed_keys)

        for direction in input_handler.consume_player_one():
            service.queue_direction_change(state.player_one, direction)
        for direction in input_handler.consume_player_two():
            service.queue_direction_change(state.player_two, direction)

        service.update()
        if not state.running:
            # Allow the players to read the final screen before exiting.
            pygame.time.wait(1500)
            running = False

        clock.tick(config.frame_rate)

    display.close()

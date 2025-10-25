"""Pygame based adapters that satisfy the application ports."""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import pygame

from tron_game.application.ports import ClockPort, DisplayPort
from tron_game.domain.player import Player
from tron_game.domain.trail import Trail

Color = Tuple[int, int, int]


class PygameDisplay(DisplayPort):
    """Concrete adapter that renders the game using Pygame."""

    def __init__(
        self,
        window_size: tuple[int, int],
        background_color: Color = (0, 0, 0),
        caption: str = "Tron Legacy",
        font_path: Optional[Path] = None,
    ) -> None:
        pygame.init()
        self._window = pygame.display.set_mode(window_size)
        pygame.display.set_caption(caption)
        self._font_large = pygame.font.Font(str(font_path) if font_path else None, 96)
        self._font_medium = pygame.font.Font(str(font_path) if font_path else None, 48)
        self.background_color = background_color
        self._window_size = window_size

    def clear(self) -> None:
        self._window.fill(self.background_color)

    def draw_player(self, player: Player) -> None:
        rect = player.as_rect()
        pygame.draw.rect(
            self._window,
            player.color,
            pygame.Rect(int(rect[0]), int(rect[1]), rect[2], rect[3]),
        )

    def draw_trail(self, player: Player, trail: Trail) -> None:
        if len(trail.points) < 2:
            return
        for start, end in trail.segments():
            pygame.draw.line(
                self._window,
                player.color,
                (int(start[0]), int(start[1])),
                (int(end[0]), int(end[1])),
                trail.width,
            )

    def draw_game_over(self, winner: Optional[Player]) -> None:
        overlay = pygame.Surface(self._window_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self._window.blit(overlay, (0, 0))
        game_over_text = self._font_large.render("GAME OVER", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(self._window_size[0] // 2, self._window_size[1] // 2))
        self._window.blit(game_over_text, text_rect)
        if winner:
            winner_text = self._font_medium.render(f"{winner.name} wins", True, winner.color)
            winner_rect = winner_text.get_rect(center=(self._window_size[0] // 2, self._window_size[1] // 2 + 100))
            self._window.blit(winner_text, winner_rect)

    def update(self) -> None:
        pygame.display.flip()

    def sample_color(self, position: tuple[int, int]) -> Color:
        x, y = position
        if x < 0 or y < 0 or x >= self._window_size[0] or y >= self._window_size[1]:
            return (255, 255, 255)
        return self._window.get_at((x, y))[:3]

    def close(self) -> None:
        pygame.quit()


class PygameClock(ClockPort):
    """Adapter around :class:`pygame.time.Clock`."""

    def __init__(self) -> None:
        self._clock = pygame.time.Clock()

    def tick(self, frame_rate: int) -> None:
        self._clock.tick(frame_rate)

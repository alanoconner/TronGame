"""Application services encapsulating game rules."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

from tron_game.application.ports import DisplayPort
from tron_game.domain.direction import Direction
from tron_game.domain.game_state import GameState
from tron_game.domain.player import Player
from tron_game.domain.trail import Trail

GridPoint = Tuple[int, int]


@dataclass
class GamePair:
    """Helper structure used to iterate over player/trail combinations."""

    player: Player
    trail: Trail


class GameService:
    """Coordinates domain objects and rendering through well-defined ports."""

    def __init__(self, state: GameState, display: DisplayPort, board_size: tuple[int, int]) -> None:
        self.state = state
        self.display = display
        self.board_width, self.board_height = board_size
        self._direction_changes: Dict[str, Direction] = {}
        self._occupied_positions: Dict[str, set[GridPoint]] = {
            state.player_one.name: {self._to_grid_point(p) for p in state.trail_one.points},
            state.player_two.name: {self._to_grid_point(p) for p in state.trail_two.points},
        }

    def queue_direction_change(self, player: Player, new_direction: Direction) -> None:
        """Queue a direction change, validating the move before applying it."""
        if new_direction is player.direction:
            return
        if new_direction is player.direction.opposite():
            return
        self._direction_changes[player.name] = new_direction

    def update(self) -> None:
        """Update the game state and render the next frame."""
        if not self.state.running:
            self.display.clear()
            self.display.draw_game_over(self.state.winner)
            self.display.update()
            return

        self._apply_direction_changes()
        collisions = list(self._advance_players())
        self._render_scene()
        for player, collided in collisions:
            if collided:
                self.state.running = False
                self.state.winner = self._other_player(player)
                break

    def _apply_direction_changes(self) -> None:
        for player in (self.state.player_one, self.state.player_two):
            if player.name in self._direction_changes:
                player.direction = self._direction_changes[player.name]
                player.start_new_segment()
                self._pairs_by_name[player.name].trail.add_point(player.position)
        self._direction_changes.clear()

    def _advance_players(self) -> Iterable[tuple[Player, bool]]:
        for pair in self._pairs:
            pair.player.move()
            pair.trail.add_point(pair.player.position)
            grid_point = self._to_grid_point(pair.player.position)
            collided = self._is_out_of_bounds(pair.player) or self._is_collision(pair.player, grid_point)
            self._occupied_positions[pair.player.name].add(grid_point)
            yield pair.player, collided

    def _render_scene(self) -> None:
        self.display.clear()
        for pair in self._pairs:
            self.display.draw_trail(pair.player, pair.trail)
            self.display.draw_player(pair.player)
        self.display.update()

    def _is_out_of_bounds(self, player: Player) -> bool:
        x, y = player.position
        if x < player.radius or y < player.radius:
            return True
        if x > self.board_width - player.radius:
            return True
        if y > self.board_height - player.radius:
            return True
        return False

    def _is_collision(self, player: Player, grid_point: GridPoint) -> bool:
        opponent = self._other_player(player)
        opponent_points = self._occupied_positions[opponent.name]
        if grid_point in opponent_points:
            return True
        own_points = self._occupied_positions[player.name]
        # Exclude the most recent position to prevent self-collision at the start of movement.
        if grid_point in own_points:
            return True
        return False

    def _other_player(self, player: Player) -> Player:
        return self.state.player_two if player is self.state.player_one else self.state.player_one

    @property
    def _pairs(self) -> tuple[GamePair, GamePair]:
        return (
            GamePair(self.state.player_one, self.state.trail_one),
            GamePair(self.state.player_two, self.state.trail_two),
        )

    @property
    def _pairs_by_name(self) -> Dict[str, GamePair]:
        return {pair.player.name: pair for pair in self._pairs}

    @staticmethod
    def _to_grid_point(position: tuple[float, float]) -> GridPoint:
        """Quantise a position so fractional steps remain unique."""
        scale = 10  # Matches the rounding precision applied when players move.
        return int(round(position[0] * scale)), int(round(position[1] * scale))

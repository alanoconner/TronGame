# Architecture Overview

The application follows a clean architecture layout where the inner layers (domain and application) have no knowledge of frameworks. Dependencies always point inwards, enabling straightforward unit testing and experimentation with alternative user interfaces.

## Layers

1. **Domain (`tron_game/domain/`)**
   - Contains pure Python entities such as `Player`, `Trail`, and supporting value objects.
   - Rules are expressed through rich domain models with meaningful methods (`Player.move`).

2. **Application (`tron_game/application/`)**
   - Implements use cases in `GameService`, orchestrating domain objects and enforcing business rules such as collision detection.
   - Communicates with the outside world through ports (`DisplayPort`, `ClockPort`).

3. **Infrastructure (`tron_game/infrastructure/`)**
   - Provides the adapters required to fulfil the ports. `PygameDisplay` renders the state, while `PygameClock` keeps a consistent frame rate.

4. **Presentation (`tron_game/presentation/`)**
   - Houses the delivery mechanism (`game_loop.run`) that coordinates user input, the application service, and rendering.

## Key Design Decisions

- **Directional Input Queue:** `InputHandler` queues key presses per player so that fast turn combinations are never missed.
- **Deterministic Collision Checking:** Instead of reading pixel data, the game tracks occupied grid points for each player. This keeps the domain logic deterministic and testable.
- **Explicit Configuration:** All tweakable constants (window size, player speed, colours) reside in `GameConfig`, making the game easy to customise.

## Extending the Game

- To change controls or add AI, start with the presentation layer.
- To adjust physics or collision logic, update `GameService` in the application layer.
- To switch rendering libraries (e.g., to a web framework), implement a new adapter that satisfies `DisplayPort` and plug it into the presentation layer.

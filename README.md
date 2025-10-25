# Tron Game (Python)

A two-player light cycle battle inspired by *Tron: Legacy*. The project demonstrates a clean architecture approach with clear separation between the domain model, application services, infrastructure adapters, and presentation logic. It is designed to be interview-ready with comprehensive documentation and type-safe Python code.

## Features

- 🕹️ Local multiplayer action for two players using keyboard controls.
- 🧱 Deterministic collision handling using a domain-first approach instead of pixel sampling.
- 🧩 Clean architecture and SOLID principles applied across the codebase.
- 🧪 Fully type annotated code with docstrings to aid readability.

## Project Structure

```
tron_game/
├── application/        # Use cases and services coordinating the domain
├── domain/             # Enterprise business rules (entities and value objects)
├── infrastructure/     # Framework and driver adapters (Pygame)
└── presentation/       # Delivery mechanism orchestrating the event loop
```

Additional documentation can be found in the [`docs/`](docs/) directory.

## Getting Started

### Prerequisites

- Python 3.11+
- [Pygame](https://www.pygame.org/news)

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`
pip install -r requirements.txt
```

### Running the Game

```bash
python main.py
```

### Controls

| Player | Up | Down | Left | Right |
| ------ | -- | ---- | ---- | ----- |
| Green Rider | W | S | A | D |
| Red Rider | ↑ | ↓ | ← | → |

### Exiting

Close the game window or press <kbd>Esc</kbd> to quit.

## Design Overview

The goal of this refactor was to create a codebase that is easy to explain during a technical interview. Key aspects include:

- **Single Responsibility Principle:** Each class has one reason to change. For example, `GameService` contains the game rules, while `PygameDisplay` only worries about rendering.
- **Open/Closed Principle:** Behaviour can be extended (e.g., swapping the renderer) without modifying core domain classes.
- **Dependency Inversion:** High-level modules depend on abstractions (`DisplayPort`), enabling easy substitution in tests.
- **Separation of Concerns:** Presentation code orchestrates the application without mixing in game rules or rendering logic.

## Testing and Development Tips

- Run `python -m pygame.examples.aliens` to verify your Pygame installation.
- When modifying input handling, adjust `InputHandler` in `tron_game/presentation/game_loop.py`.
- Game rules and collision behaviour live in `tron_game/application/game_service.py`.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

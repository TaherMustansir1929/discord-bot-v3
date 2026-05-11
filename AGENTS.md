# Repository Guidelines

## Project Structure & Module Organization

`main.py` is the Discord bot entrypoint. It loads environment variables, configures Discord intents, registers slash commands, and delegates behavior to handlers. Feature code lives under `src/handlers/`, with one package per command area such as `giphy`, `imagine`, `roast`, `speech`, and `waifu`. Shared helpers belong in `src/utils/`, and reusable prompt text belongs in `src/prompts/`. Experimental work is kept in `notebooks/`. Deployment assets live at the repository root, including `Dockerfile` and `deploy.sh`.

## Build, Test, and Development Commands

- `uv sync`: install runtime and development dependencies from `pyproject.toml` and `uv.lock`.
- `uv run python main.py`: run the bot locally using values from `.env`.
- `uv run ruff check .`: run Ruff lint and import-order checks.
- `uv run ty check .`: run static type checks.
- `docker build -t discord-bot-v3 .`: build the container image.
- `docker run --env-file .env discord-bot-v3`: run the bot in Docker with local secrets.

## Coding Style & Naming Conventions

Use Python 3.13, 4-space indentation, and Ruff's configured 88-character line length. Ruff currently enforces `E`, `F`, and `I` rules, so keep imports sorted and remove unused code. Use `snake_case` for modules, functions, variables, and handler names. Keep command-specific behavior inside its handler package, and move cross-command logic into `src/utils/`.

## Testing Guidelines

No test suite is currently present. Add new tests under `tests/` using `test_*.py` naming. Prefer pytest-style tests, including async tests for Discord handlers when needed. Before submitting changes, run at least `uv run ruff check .` and `uv run ty check .`.

## Commit & Pull Request Guidelines

Follow the existing commit style: short, imperative, lowercase summaries such as `implement speech command` or `fix fetch_image() call`. Pull requests should include a concise description, affected bot commands, required environment variables, and screenshots or sample Discord output for user-visible behavior.

## Security & Configuration Tips

Store secrets in `.env` and do not commit them. The code reads keys such as `DISCORD_TOKEN`, `GIPHY_API_KEY`, `BFL_API_KEY`, `GROQ_API_KEY`, and `GOOGLE_API_KEY`. Keep deployment `.env` files outside shared history and verify required keys before running Docker or `main.py`.

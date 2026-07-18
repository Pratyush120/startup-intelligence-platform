# Contributing to Strategic Decision Intelligence Platform (SDIP)

First off, thank you for considering contributing to SDIP! It's people like you that make SDIP such a great tool.

## Getting Started

1. Fork the repository and create your branch from `main`.
2. Ensure you have Python 3.10+ and Node.js 18+ installed.
3. Install dependencies:
   - Backend: `pip install -r requirements.txt` (or via `poetry`)
   - Frontend: `npm install`
4. Make sure your code passes the current tests: `pytest tests/`

## Code Standards

- **Backend**: We use `ruff` for both linting and formatting. Run `ruff format src/` and `ruff check src/` before submitting.
- **Frontend**: We use Prettier and ESLint.
- **Testing**: Maintain or improve test coverage. New features must include relevant unit or integration tests.
- **Architecture**: Adhere to the existing Repository and Provider patterns. Avoid adding external dependencies unless absolutely necessary.

## Submitting Changes

1. Open a Pull Request with a clear title and description.
2. Link any relevant issues.
3. Wait for the CI pipeline to pass.
4. A maintainer will review your code.

Thank you for your contributions!

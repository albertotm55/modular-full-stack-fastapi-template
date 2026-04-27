# Repository Guidelines

## Project Structure & Module Organization

This is a full-stack FastAPI template. Backend code lives in `backend/app`: API routes are in `api/routes`, settings and database helpers in `core`, SQLModel models in `models.py`, and Alembic migrations in `alembic/versions`. Backend tests are in `backend/tests`.

The frontend is a Vite React app in `frontend`. Routes live in `src/routes`, components in `src/components`, hooks in `src/hooks`, generated API client files in `src/client`, and Playwright tests in `frontend/tests`.

## Build, Test, and Development Commands

- `docker compose up -d`: start the local stack.
- `./scripts/test-local.sh`: rebuild Docker and run backend tests in the backend container.
- `cd backend && bash scripts/test.sh`: run backend pytest with coverage reports.
- `cd backend && bash scripts/lint.sh`: run `mypy`, `ty`, Ruff, and format checks.
- `cd backend && bash scripts/format.sh`: auto-fix Ruff issues and format backend code.
- `bun run dev`: start the frontend dev server from the root workspace.
- `bun run lint`: run frontend Biome checks and fixes.
- `bun run test` / `bun run test:ui`: run Playwright tests headlessly or with the UI.
- `cd frontend && bun run build`: type-check and build the frontend.

## Coding Style & Naming Conventions

Backend Python targets 3.10+ with strict `mypy`, `ty`, and Ruff. Use 4-space indentation, typed functions, snake_case functions/modules, PascalCase classes, and existing SQLModel patterns.

Frontend TypeScript uses Biome with space indentation, double quotes, and omitted semicolons where valid. Name components in PascalCase, hooks as `useSomething`, and route files by URL segment. Do not hand-edit `frontend/src/client`; regenerate it.

## Testing Guidelines

Backend tests use pytest and coverage. Add tests near changed behavior with `test_*.py` filenames and clear function names. Frontend end-to-end tests use Playwright specs in `frontend/tests/*.spec.ts`; update specs for visible workflow changes.

## Commit & Pull Request Guidelines

Recent commits use short, imperative messages often prefixed with an emoji, for example `📝 Update release notes` or `🔒 Pin GitHub actions by commit SHA (#2246)`.

For PRs, keep scope to one change, describe motivation and implementation, link issues or discussions, and include screenshots for UI changes. Update tests and docs when behavior changes. For large features or architecture changes, start with a GitHub Discussion as described in `CONTRIBUTING.md`.

## Security & Configuration Tips

Do not commit secrets, local `.env` files, generated credentials, or private deployment values. Review `SECURITY.md`, `development.md`, and `deployment.md` before changing authentication, email, database, Docker, or deployment behavior.

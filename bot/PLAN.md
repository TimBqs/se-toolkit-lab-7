# LMS Telegram Bot - Development Plan

## Overview

This bot provides a Telegram interface to the LMS backend, allowing students to check labs, scores, and ask questions using natural language. The development is split into 4 tasks: scaffolding, backend integration, LLM-powered intent routing, and Docker deployment.

## Task 1: Plan and Scaffold (Current)

**Goal:** Create testable project structure with `--test` mode.

**Architecture:**
- `bot.py` - Entry point with CLI `--test` mode and Telegram startup
- `handlers/` - Command handlers as pure functions (no Telegram dependency)
- `services/` - External API clients (LMS API, LLM API)
- `config.py` - Environment variable loading via pydantic-settings

**Key Pattern:** Separation of concerns. Handlers are plain functions that take input and return text. They work identically from `--test` mode, unit tests, or Telegram. This makes testing trivial and keeps transport logic separate from business logic.

**Test Mode:** `uv run bot.py --test "/start"` calls handlers directly without Telegram connection.

## Task 2: Backend Integration

**Goal:** Connect handlers to the LMS backend API.

**Implementation:**
- Create `services/lms_client.py` with Bearer token authentication
- Update `/health` to ping the backend
- Update `/labs` to fetch available labs
- Update `/scores <lab>` to fetch student scores

**Key Pattern:** API client abstraction. Handlers call `lms_client.get_labs()` instead of making HTTP requests directly. This makes testing easier (mock the client) and keeps HTTP logic centralized.

**Environment:** `LMS_API_BASE_URL` and `LMS_API_KEY` from `.env.bot.secret`.

## Task 3: LLM Intent Routing

**Goal:** Support natural language queries like "what labs are available?"

**Implementation:**
- Create `services/llm_client.py` for LLM API calls
- Define tool descriptions for each handler
- Use LLM to parse user input and route to appropriate handler
- Fallback to "I don't understand" for unrecognized intents

**Key Pattern:** Tool calling. The LLM receives tool descriptions and decides which handler to call based on user input. The fix for wrong routing is improving tool descriptions, not adding regex fallbacks.

**Example Flow:**
1. User: "what labs can I do?"
2. LLM analyzes input, matches to `handle_labs` tool
3. Bot calls `handle_labs()` and returns result

## Task 4: Docker Deployment

**Goal:** Containerize the bot for production deployment.

**Implementation:**
- Create `bot/Dockerfile` with multi-stage build
- Update `docker-compose.yml` to include bot service
- Configure Docker networking (containers use service names, not localhost)
- Set up health checks and restart policies

**Key Pattern:** Docker networking. Inside Docker, `http://backend:8000` reaches the backend container, not `http://localhost:8000`.

## File Structure

```
bot/
├── bot.py              # Entry point (--test + Telegram)
├── config.py           # Environment loading
├── pyproject.toml      # Dependencies
├── PLAN.md             # This file
├── handlers/
│   └── __init__.py     # Command handlers
└── services/
    ├── lms_client.py   # LMS API client (Task 2)
    └── llm_client.py   # LLM API client (Task 3)
```

## Testing Strategy

1. **Unit tests:** Test handlers in isolation (pytest)
2. **Test mode:** Manual testing via `--test` flag
3. **Integration tests:** Test against real backend (e2e)
4. **Telegram testing:** Manual testing in real Telegram

## Deployment Checklist

- [ ] `.env.bot.secret` exists with BOT_TOKEN, LMS_API_KEY, LLM_API_KEY
- [ ] `uv sync` succeeds
- [ ] `--test` mode works for all commands
- [ ] Docker build succeeds
- [ ] Bot responds in Telegram

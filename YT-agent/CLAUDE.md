# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A German-language customer support chatbot for **Sandras Friseurwagon** (mobile hair salon, Waldegg, Austria) built with the Claude Agent SDK. Uses `ClaudeSDKClient` for multi-turn conversations.

## Running the agent

```bash
# Prerequisite: Claude Code CLI must be installed
npm install -g @anthropic-ai/claude-code

# Set up environment
cp .env.example .env
# Edit .env and insert your ANTHROPIC_API_KEY

# Run
.venv/bin/python main.py
```

The venv at `.venv/` is pre-installed with all dependencies.

## Architecture

Two files hold all logic:

- **`config.py`** — The system prompt (`SYSTEM_PROMPT`). This is the primary place to tune agent behavior, add new business info, or change the tone.
- **`main.py`** — `ClaudeSDKClient` loop: connects once, loops on user input, streams `AssistantMessage`/`ResultMessage` back. `build_options()` is where tools, model, and turn limits are configured.

The agent is intentionally restricted to `WebFetch` and `WebSearch` only — no file system access. It can fetch live data from `friseurwagon.com` during conversations.

## Key configuration (main.py `build_options`)

| Setting | Value | Reason |
|---------|-------|--------|
| `model` | `claude-haiku-4-5` | Fast and cost-effective for support |
| `allowed_tools` | `WebFetch`, `WebSearch` | Read-only; no write access |
| `permission_mode` | `default` | No auto-approval needed |
| `max_turns` | 30 | Resets each new `ClaudeSDKClient` session |

## Updating business information

Business details (address, phone, services) live in `config.py` → `SYSTEM_PROMPT`. Edit that string to reflect changes — no code changes needed elsewhere.

## Dependencies

- `claude-agent-sdk==0.1.50` — requires Claude Code CLI to be installed separately
- `python-dotenv==1.1.0` — loads `ANTHROPIC_API_KEY` from `.env`

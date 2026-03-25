# coding-agents-loop

Multi-agent coding system with 3 coordinated agents (Orchestrator, Coder, Reviewer) running in a review loop until the code is approved.

```
┌─────────────────────────────────────────────────────────────┐
│                    docker-compose                           │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  CLIProxyAPI │    │   LiteLLM    │    │    Agents    │  │
│  │  :8080       │◄───│   :4000      │◄───│  (Agno +    │  │
│  │              │    │              │    │  Claude CLI) │  │
│  │ Gemini OAuth │    │ orchestrator │    │              │  │
│  │ Claude OAuth │    │ → Gemini 2.5 │    │ Orchestrator │  │
│  │ Codex OAuth  │    │ coder        │    │ Coder        │  │
│  │ (multi-acct) │    │ → Codex      │    │ Reviewer     │  │
│  └──────────────┘    │ reviewer     │    └──────────────┘  │
│                      │ → Sonnet     │                       │
│                      └──────────────┘                       │
└─────────────────────────────────────────────────────────────┘
              │
              ▼ /workspace (volume condiviso con host WSL2)
```

## Stack

| Component | Role |
|-----------|------|
| [CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) | Go proxy — unifies Google Cloud Pro (Gemini), ChatGPT Pro (Codex), Claude via OAuth. No API keys needed. |
| [LiteLLM](https://github.com/BerriAI/litellm) | OpenAI-compatible model router mapping aliases → backends via CLIProxyAPI |
| [Agno Framework](https://github.com/agno-agi/agno) | Python framework coordinating the 3 agents as a Team with `mode="coordinate"` |
| Claude Code CLI | Execution engine for all 3 agents |

## Agents

| Agent | Model | LiteLLM alias | Role |
|-------|-------|---------------|------|
| Orchestrator | Gemini 2.5 Pro | `orchestrator` | Decomposes tasks, assigns to Coder, iterates until approved |
| Coder | OpenAI Codex | `coder` | Implements code using filesystem/shell/git tools and MCP servers |
| Reviewer | Claude Sonnet 4 | `reviewer` | Reviews output, returns issues in Italian or approves with "APPROVATO" |

## The Loop

```
User Task → Orchestrator → Coder → Reviewer
                ↑                      |
                |  APPROVATO           | issues found
                └──────────────────────┘
                     ↓ (loop, max MAX_REVIEW_ITERATIONS, default 5)
                  Coder (fixes issues with context)
```

**Language rule:** agents communicate with each other in English (more efficient for LLMs). All final output to the user is in Italian.

## Prerequisites

- Docker Desktop with WSL2 backend
- `tmux`: `sudo apt install tmux`
- Active subscriptions: Google Cloud Pro, ChatGPT Pro, Claude Pro

## Setup

```bash
git clone https://github.com/Thomas-Piva/coding-agents-loop
cd coding-agents-loop

cp .env.example .env
cp cliproxy/config.example.yaml cliproxy/config.yaml

# Authenticate each provider (run once)
make login-gemini
make login-claude
make login-codex

# Start all services
make up
make ps
```

## Usage with Tmux

```bash
chmod +x tmux-start.sh

# Open monitoring session (no task)
make tmux

# Run a task
./tmux-start.sh "Build a Flask REST API with /health and /items endpoints"

# Use a template
./tmux-start.sh "template:webapp"
./tmux-start.sh "template:api_service"
./tmux-start.sh "template:refactor"
```

**Tmux navigation:** `Ctrl+B` arrows to move between panes, `Ctrl+B Z` to zoom, `Ctrl+B D` to detach, `tmux attach -t coding-agents` to reattach.

## Available Templates

| Template | Description |
|----------|-------------|
| `template:webapp` | Full-stack web application (frontend + backend + DB) |
| `template:api_service` | Production REST API with auth, validation, OpenAPI docs |
| `template:refactor` | Analyze and refactor existing code in /workspace |

## Extending the System

- **New agent:** create `agents/agents/myagent.py`, add to `dev_team.py`, add alias in `litellm/config.yaml`
- **New tool:** create `agents/tools/mytool.py`, import in the relevant agent
- **New MCP server:** add entry in `agents/mcp_servers/config.json`
- **New template:** create `agents/tasks/mytemplate.yaml` with fields: `name`, `description`, `orchestrator_prompt`, `coder_focus`, `reviewer_checklist`

## Makefile targets

```
make up            # Start all containers
make down          # Stop containers
make build         # Rebuild agents image
make tmux          # Open tmux monitoring session
make run TASK="…"  # Run a task
make logs          # Tail all logs
make ps            # Show container status
make clean         # Clear workspace
make login-gemini  # OAuth login for Gemini
make login-claude  # OAuth login for Claude
make login-codex   # OAuth login for Codex
```

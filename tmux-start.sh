#!/bin/bash
# Avvia sessione tmux con tutti gli agenti visibili in pane separati.
# Uso: ./tmux-start.sh [task opzionale]
# Es:  ./tmux-start.sh "Build a Flask REST API"
# Es:  ./tmux-start.sh "template:webapp"

SESSION="coding-agents"
TASK="${1:-}"

if ! command -v tmux &> /dev/null; then
  echo "tmux non trovato. Installa con: sudo apt install tmux"
  exit 1
fi

if ! docker-compose ps 2>/dev/null | grep -q "Up"; then
  echo "Container non in esecuzione. Avvia prima: docker-compose up -d"
  exit 1
fi

# Kill existing session if present
tmux kill-session -t "$SESSION" 2>/dev/null

# Create new session (detached)
tmux new-session -d -s "$SESSION" -x "$(tput cols)" -y "$(tput lines)"
tmux rename-window -t "$SESSION:0" "DevTeam"

# ── Pane 0 (left top): Orchestrator + System logs
tmux send-keys -t "$SESSION:0.0" \
  "clear && echo '=== ORCHESTRATOR (Gemini 2.5 Pro) ===' && \
   docker-compose logs -f agents | grep --line-buffered '\[ORCHESTRATOR\]\|\[SYSTEM\]'" C-m

# ── Pane 1 (right): Coder logs
tmux split-window -h -t "$SESSION:0.0"
tmux send-keys -t "$SESSION:0.1" \
  "clear && echo '=== CODER (Codex) ===' && \
   docker-compose logs -f agents | grep --line-buffered '\[CODER\]'" C-m

# ── Pane 2 (right middle): Reviewer logs
tmux split-window -v -t "$SESSION:0.1"
tmux send-keys -t "$SESSION:0.2" \
  "clear && echo '=== REVIEWER (Claude Sonnet) ===' && \
   docker-compose logs -f agents | grep --line-buffered '\[REVIEWER\]'" C-m

# ── Pane 3 (right lower): LiteLLM routing
tmux split-window -v -t "$SESSION:0.2"
tmux send-keys -t "$SESSION:0.3" \
  "clear && echo '=== LITELLM ROUTING ===' && \
   docker-compose logs -f litellm" C-m

# ── Pane 4 (right bottom): CLIProxyAPI logs
tmux split-window -v -t "$SESSION:0.3"
tmux send-keys -t "$SESSION:0.4" \
  "clear && echo '=== CLIPROXY LOGS ===' && \
   docker-compose logs -f cliproxy" C-m

# ── Pane 5 (left bottom): Workspace file watcher
tmux split-window -v -t "$SESSION:0.0"
tmux send-keys -t "$SESSION:0.5" \
  "watch -n2 'echo \"=== WORKSPACE ===\"; \
   find workspace/ -type f 2>/dev/null | sed \"s|workspace/||\" | sort || \
   echo \"workspace vuoto\"'" C-m

# ── Optional: Task runner window
if [ -n "$TASK" ]; then
  tmux new-window -t "$SESSION:1" -n "Task Runner"
  tmux send-keys -t "$SESSION:1" \
    "docker-compose exec agents python main.py \"$TASK\" && \
     echo '=== TASK COMPLETATO ===' && read" C-m
  tmux select-window -t "$SESSION:0"
fi

# Apply custom tmux layout/theme if present
tmux source-file tmux-layout.conf 2>/dev/null || true

tmux select-pane -t "$SESSION:0.0"
tmux attach-session -t "$SESSION"

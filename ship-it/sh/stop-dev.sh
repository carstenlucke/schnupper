#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIR_NAME="$(basename "$ROOT_DIR")"
# Sanitize: tmux session names must not contain dots or colons
SESSION="rsrc-${DIR_NAME//[.:]/-}"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux kill-session -t "$SESSION"
  echo "Session '$SESSION' beendet."
else
  echo "Keine aktive Session '$SESSION' gefunden."
fi

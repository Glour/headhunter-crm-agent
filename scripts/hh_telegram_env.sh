#!/usr/bin/env bash
set -euo pipefail

HH_TELEGRAM_PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$HH_TELEGRAM_PROJECT_ROOT"

# shellcheck source=load_project_env.sh
source "$HH_TELEGRAM_PROJECT_ROOT/scripts/load_project_env.sh"

# Preserve explicit caller overrides when sourcing the local secrets file. This lets
# watchdog/cron force safe runtime flags such as HH_TELEGRAM_SEND_ON_START=0 even
# if the secrets file contains a different default.
__hh_override_names=(
  HH_CRM_DB_PATH
  HH_TELEGRAM_SEND_ON_START
  HH_TELEGRAM_CHAT_ID_PATH
  HH_TELEGRAM_OFFSET_PATH
  HH_TELEGRAM_RUN_LOCK_PATH
  HH_TELEGRAM_MIN_SCORE
  HH_TELEGRAM_LIMIT
  HH_TELEGRAM_PER_QUERY
  HH_TELEGRAM_DRAFT_THRESHOLD
  HH_TELEGRAM_POLL_TIMEOUT
  HH_TELEGRAM_QUERIES
  HH_TELEGRAM_PYTHON
  HH_TELEGRAM_CHAT_ID
  HH_CHAT_REPLY_SEND
  HH_CHAT_REPLY_ALLOW_LIVE_SEND
  HH_CHAT_EXTERNAL_SUBMIT
  HH_CHAT_REPLY_HEADLESS
  HH_CHAT_REPLY_LIMIT
  HH_CHAT_REPLY_MAX_CHATS
  HH_CHAT_REPLY_STATE_FILE
  HH_CHAT_REPLY_PYTHON
)
__hh_override_keys=(__sentinel)
__hh_override_values=('')
for __hh_key in "${__hh_override_names[@]}"; do
  if declare -p "$__hh_key" >/dev/null 2>&1; then
    __hh_override_keys+=("$__hh_key")
    __hh_override_values+=("${!__hh_key}")
  fi
done

SECRETS_FILE="${HH_TELEGRAM_SECRETS_FILE:-./.secrets/hh_telegram.env}"
if [[ -f "$SECRETS_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$SECRETS_FILE"
  set +a
fi

__hh_index=0
for __hh_key in "${__hh_override_keys[@]}"; do
  if [[ "$__hh_index" -gt 0 ]]; then
    export "$__hh_key=${__hh_override_values[$__hh_index]}"
  fi
  __hh_index=$((__hh_index + 1))
done
unset __hh_key __hh_index __hh_override_keys __hh_override_values __hh_override_names

export PYTHONPATH="${PYTHONPATH:-backend}"
export HH_CRM_DB_PATH="${HH_CRM_DB_PATH:-./data/hh_crm.sqlite3}"
export HH_TELEGRAM_CHAT_ID_PATH="${HH_TELEGRAM_CHAT_ID_PATH:-./data/hh_telegram_chat_id.txt}"
export HH_TELEGRAM_OFFSET_PATH="${HH_TELEGRAM_OFFSET_PATH:-./data/hh_telegram_offset.txt}"
export HH_TELEGRAM_RUN_LOCK_PATH="${HH_TELEGRAM_RUN_LOCK_PATH:-./data/hh_telegram_run.lock}"

if [[ -z "${HH_TELEGRAM_PYTHON:-}" ]]; then
  if [[ -x /usr/local/lib/hermes-agent/venv/bin/python3 ]]; then
    HH_TELEGRAM_PYTHON=/usr/local/lib/hermes-agent/venv/bin/python3
  elif command -v python3 >/dev/null 2>&1; then
    HH_TELEGRAM_PYTHON="$(command -v python3)"
  elif [[ -x /usr/bin/python3 ]]; then
    HH_TELEGRAM_PYTHON=/usr/bin/python3
  elif command -v python >/dev/null 2>&1; then
    HH_TELEGRAM_PYTHON="$(command -v python)"
  else
    echo "HH Telegram: no Python interpreter found" >&2
    exit 127
  fi
fi
export HH_TELEGRAM_PYTHON

mkdir -p ./data ./logs

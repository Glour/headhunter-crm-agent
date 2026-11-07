#!/usr/bin/env bash
# Source optional .env from project root without clobbering variables explicitly
# provided by the caller, for example: HH_CHAT_REPLY_SEND=0 scripts/run_...
# Must be sourced after cd to the repository root.

if [[ -f .env ]]; then
  # Indexed arrays also work with the Bash version shipped with macOS.
  # The sentinel keeps an empty array safe under `set -u` in Bash 3.
  __hh_project_env_names=(__sentinel)
  __hh_project_env_values=('')
  while IFS='=' read -r __hh_project_env_name _; do
    case "$__hh_project_env_name" in
      HH_*|PYTHONPATH|VITE_*)
        __hh_project_env_names+=("$__hh_project_env_name")
        __hh_project_env_values+=("${!__hh_project_env_name-}")
        ;;
    esac
  done < <(env)

  set -a
  # shellcheck disable=SC1091
  source .env
  set +a

  __hh_project_env_index=0
  for __hh_project_env_name in "${__hh_project_env_names[@]}"; do
    if [[ "$__hh_project_env_index" -gt 0 ]]; then
      export "$__hh_project_env_name=${__hh_project_env_values[$__hh_project_env_index]}"
    fi
    __hh_project_env_index=$((__hh_project_env_index + 1))
  done
  unset __hh_project_env_name __hh_project_env_index __hh_project_env_names __hh_project_env_values
fi

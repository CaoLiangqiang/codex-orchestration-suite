#!/usr/bin/env bash
set -euo pipefail

REPOSITORY="${CODEX_ORCHESTRATION_REPOSITORY:-CaoLiangqiang/codex-orchestration-suite}"
REF="${CODEX_ORCHESTRATION_REF:-main}"
CODEX_DIR="${CODEX_HOME:-${HOME}/.codex}"
AGENTS_DIR="${CODEX_DIR}/agents"
SKILL_SOURCE="https://github.com/${REPOSITORY}/tree/${REF}"
PROFILE_BASE_URL="https://raw.githubusercontent.com/${REPOSITORY}/${REF}/skills/team-mode/assets/agent-profiles"
PROFILE_NAMES=(
  "Complex Executor.toml"
  "Executor.toml"
  "Explorer.toml"
  "Reviewer.toml"
  "default.toml"
)

for command_name in cmp curl install mktemp npx python3; do
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "error: required command not found: ${command_name}" >&2
    exit 1
  fi
done

temporary_dir="$(mktemp -d)"
trap 'rm -rf -- "${temporary_dir}"' EXIT
profile_download_dir="${temporary_dir}/agent-profiles"
mkdir -p "${profile_download_dir}"

echo "Downloading Team Mode Agent profiles from ${REPOSITORY}@${REF}..."
for profile_name in "${PROFILE_NAMES[@]}"; do
  curl --fail --silent --show-error --location \
    "${PROFILE_BASE_URL}/${profile_name// /%20}" \
    --output "${profile_download_dir}/${profile_name}"
done

python3 - "${profile_download_dir}" <<'PY'
import sys
import tomllib
from pathlib import Path

profile_dir = Path(sys.argv[1])
expected = {
    "Complex Executor.toml": "Complex Executor",
    "Executor.toml": "Executor",
    "Explorer.toml": "Explorer",
    "Reviewer.toml": "Reviewer",
    "default.toml": "default",
}

for filename, expected_name in expected.items():
    path = profile_dir / filename
    with path.open("rb") as profile_file:
        profile = tomllib.load(profile_file)
    if profile.get("name") != expected_name:
        raise SystemExit(f"error: {filename} has unexpected Agent name")
    for key in ("description", "model", "model_reasoning_effort", "sandbox_mode", "developer_instructions"):
        if not profile.get(key):
            raise SystemExit(f"error: {filename} is missing {key}")
PY

conflicts=()
for profile_name in "${PROFILE_NAMES[@]}"; do
  destination="${AGENTS_DIR}/${profile_name}"
  if [[ -f "${destination}" ]] && ! cmp --silent "${profile_download_dir}/${profile_name}" "${destination}"; then
    conflicts+=("${destination}")
  elif [[ -e "${destination}" ]] && [[ ! -f "${destination}" ]]; then
    conflicts+=("${destination}")
  fi
done

if (( ${#conflicts[@]} > 0 )); then
  echo "error: existing Agent profiles differ from this release; nothing was installed:" >&2
  printf '  %s\n' "${conflicts[@]}" >&2
  echo "Review or back up those files, then run the installer again." >&2
  exit 1
fi

echo "Installing both Skills for Codex..."
npx --yes skills add "${SKILL_SOURCE}" \
  --skill orchestrate-project-sessions \
  --skill team-mode \
  --agent codex \
  --global \
  --yes

mkdir -p "${AGENTS_DIR}"
for profile_name in "${PROFILE_NAMES[@]}"; do
  destination="${AGENTS_DIR}/${profile_name}"
  if [[ -f "${destination}" ]]; then
    echo "Unchanged: ${destination}"
  else
    install -m 0644 "${profile_download_dir}/${profile_name}" "${destination}"
    echo "Installed: ${destination}"
  fi
done

echo
echo "Codex Orchestration Suite is installed. Open a new Codex task or restart Codex."

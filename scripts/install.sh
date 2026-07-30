#!/usr/bin/env bash
set -euo pipefail

REPOSITORY="${CODEX_ORCHESTRATION_REPOSITORY:-CaoLiangqiang/codex-orchestration-suite}"
REF="${CODEX_ORCHESTRATION_REF:-main}"
CODEX_DIR="${CODEX_HOME:-${HOME}/.codex}"
AGENTS_DIR="${CODEX_DIR}/agents"
SKILL_SOURCE="https://github.com/${REPOSITORY}/tree/${REF}"
PROFILE_BASE_URL="https://github.com/${REPOSITORY}/raw/refs/heads/${REF}/skills/team-mode/assets/agent-profiles"
PROFILE_NAMES=(
  "Complex Executor.toml"
  "Executor.toml"
  "Explorer.toml"
  "Reviewer.toml"
  "default.toml"
)
PROFILE_AGENT_NAMES=(
  "Complex Executor"
  "Executor"
  "Explorer"
  "Reviewer"
  "default"
)

for command_name in cmp curl grep install mktemp npx; do
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

required_profile_keys=(description model model_reasoning_effort sandbox_mode developer_instructions)
for profile_index in "${!PROFILE_NAMES[@]}"; do
  profile_name="${PROFILE_NAMES[profile_index]}"
  profile_path="${profile_download_dir}/${profile_name}"
  expected_name_line="name = \"${PROFILE_AGENT_NAMES[profile_index]}\""
  if ! grep -Fqx "${expected_name_line}" "${profile_path}"; then
    echo "error: ${profile_name} has an unexpected Agent name" >&2
    exit 1
  fi
  for required_key in "${required_profile_keys[@]}"; do
    if ! grep -Eq "^${required_key}[[:space:]]*=" "${profile_path}"; then
      echo "error: ${profile_name} is missing ${required_key}" >&2
      exit 1
    fi
  done
done

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

#!/usr/bin/env bash
set -euo pipefail

INSTALLER_VERSION="0.1.0"
SPEC_VERSION="1.0"
COMMAND_NAME="skills.network-install"
DEFAULT_REPO_URL="https://github.com/yeisme/yeisme-agent-my-skills.git"
DEFAULT_REF="main"

PROJECT_INPUT="$PWD"
REPO_URL="$DEFAULT_REPO_URL"
SOURCE_REF="$DEFAULT_REF"
if [[ -n "${YEISME_SKILLS_HOME:-}" ]]; then
  SOURCE_INPUT="$YEISME_SKILLS_HOME"
elif [[ -n "${XDG_DATA_HOME:-}" ]]; then
  SOURCE_INPUT="$XDG_DATA_HOME/yeisme-agent-my-skills"
elif [[ -n "${HOME:-}" ]]; then
  SOURCE_INPUT="$HOME/.local/share/yeisme-agent-my-skills"
else
  SOURCE_INPUT="$PWD/.yeisme-agent-my-skills"
fi
OUTPUT_MODE="summary"
SKILLS=()
LOG_FILE=""

usage() {
  cat <<'EOF'
Usage: install.sh [options]

Install Yeisme's public Skill source, initialize generic Skill governance,
and optionally activate named Skills.

Options:
  --project DIR       Project to configure. Defaults to the current directory.
  --repo URL          Git repository containing the public Skill source.
  --ref REF           Git branch, tag, or commit. Defaults to main.
  --source-dir DIR    Local checkout path for the Skill source.
  --skill NAME        Activate one Skill; repeat for multiple Skills.
  --agent             Emit stable key=value output.
  --json              Emit one JSON envelope.
  --version           Print installer version.
  -h, --help          Show this help.

Examples:
  install.sh --project /srv/app
  install.sh --project /srv/drama --skill ai-drama-router
  install.sh --project /srv/drama --skill ai-drama-router --skill creative-grill-me --skill creative-grilling
EOF
}

json_escape() {
  local value="$1"
  value=${value//\\/\\\\}
  value=${value//\"/\\\"}
  value=${value//$'\n'/\\n}
  value=${value//$'\r'/\\r}
  value=${value//$'\t'/\\t}
  printf '%s' "$value"
}

agent_value() {
  local value="$1"
  if [[ "$value" =~ ^[a-zA-Z0-9_./:@%+=,-]+$ ]]; then
    printf '%s' "$value"
  else
    printf '"%s"' "$(json_escape "$value")"
  fi
}

render_failure() {
  local code="$1"
  local message="$2"
  local suggestion="$3"
  case "$OUTPUT_MODE" in
    agent)
      printf 'spec_version=%s\n' "$SPEC_VERSION"
      printf 'mode=agent\n'
      printf 'command=%s\n' "$COMMAND_NAME"
      printf 'status=failed\n'
      printf 'error.code=%s\n' "$code"
      printf 'error.message='; agent_value "$message"; printf '\n'
      printf 'error.suggestion='; agent_value "$suggestion"; printf '\n'
      ;;
    json)
      printf '{"spec_version":"%s","mode":"json","command":"%s","status":"failed","summary":"%s","facts":{},"actions":[],"evidence":[],"data":{},"error":{"code":"%s","message":"%s","suggestion":"%s","retryable":false}}\n' \
        "$SPEC_VERSION" "$COMMAND_NAME" "$(json_escape "$message")" \
        "$(json_escape "$code")" "$(json_escape "$message")" "$(json_escape "$suggestion")"
      ;;
    summary)
      printf 'Status: failed\n' >&2
      printf 'Error: %s\n' "$message" >&2
      printf 'Recommended next step: %s\n' "$suggestion" >&2
      ;;
  esac
}

fail() {
  render_failure "$1" "$2" "$3"
  if [[ -n "$LOG_FILE" && -s "$LOG_FILE" ]]; then
    printf 'Installer log excerpt:\n' >&2
    tail -20 "$LOG_FILE" >&2
  fi
  exit 1
}

run_logged() {
  local label="$1"
  shift
  if ! "$@" >>"$LOG_FILE" 2>&1; then
    fail "step_failed" "$label failed." "Review the log excerpt, fix the reported Git or Skill manager error, then rerun the same command."
  fi
}

render_success() {
  local project_dir="$1"
  local source_dir="$2"
  local source_commit="$3"
  local skill_count="${#SKILLS[@]}"
  local manager_command project_command verify_command builder_profile
  printf -v manager_command '%q' "$source_dir/scripts/skills.sh"
  printf -v project_command '%q' "$project_dir"
  verify_command="$manager_command --project $project_command validate"
  local skill
  builder_profile="none"
  for skill in "${SKILLS[@]}"; do
    if [[ "$skill" == "yeisme-builder-profile" ]]; then
      builder_profile="yeisme-builder-profile"
      break
    fi
  done

  case "$OUTPUT_MODE" in
    agent)
      printf 'spec_version=%s\n' "$SPEC_VERSION"
      printf 'mode=agent\n'
      printf 'command=%s\n' "$COMMAND_NAME"
      printf 'status=success\n'
      printf 'fact.project='; agent_value "$project_dir"; printf '\n'
      printf 'fact.source='; agent_value "$source_dir"; printf '\n'
      printf 'fact.source_commit=%s\n' "$source_commit"
      printf 'fact.builder_profile=%s\n' "$builder_profile"
      printf 'fact.skill_count=%s\n' "$skill_count"
      local index=1
      for skill in "${SKILLS[@]}"; do
        printf 'item.skill.%d=%s\n' "$index" "$skill"
        index=$((index + 1))
      done
      printf 'action.verify='; agent_value "$verify_command"; printf '\n'
      ;;
    json)
      printf '{"spec_version":"%s","mode":"json","command":"%s","status":"success","summary":"Yeisme Skills were installed and validated.","facts":{"project":"%s","source":"%s","source_commit":"%s","builder_profile":"%s","skill_count":%s},"actions":[{"name":"verify","command":"%s"}],"evidence":[],"data":{"skills":[' \
        "$SPEC_VERSION" "$COMMAND_NAME" "$(json_escape "$project_dir")" \
        "$(json_escape "$source_dir")" "$source_commit" "$builder_profile" "$skill_count" \
        "$(json_escape "$verify_command")"
      local first=1
      for skill in "${SKILLS[@]}"; do
        [[ "$first" -eq 1 ]] || printf ','
        printf '"%s"' "$(json_escape "$skill")"
        first=0
      done
      printf ']}}\n'
      ;;
    summary)
      printf 'Status: success\n'
      printf 'Summary: Yeisme Skills were installed and validated.\n'
      printf 'Project: %s\n' "$project_dir"
      printf 'Source: %s\n' "$source_dir"
      printf 'Source commit: %s\n' "$source_commit"
      printf 'Builder profile: %s\n' "$builder_profile"
      if [[ "$skill_count" -gt 0 ]]; then
        printf 'Activated Skills:'
        for skill in "${SKILLS[@]}"; do printf ' %s' "$skill"; done
        printf '\n'
      fi
      printf 'Recommended next step: %s\n' "$verify_command"
      ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)
      [[ $# -ge 2 ]] || fail "option_value_required" "--project requires a directory." "Pass an existing project directory."
      PROJECT_INPUT="$2"; shift 2 ;;
    --repo)
      [[ $# -ge 2 ]] || fail "option_value_required" "--repo requires a Git URL." "Pass a public or authenticated Git repository URL."
      REPO_URL="$2"; shift 2 ;;
    --ref)
      [[ $# -ge 2 ]] || fail "option_value_required" "--ref requires a branch, tag, or commit." "Pass an explicit Git ref such as main, v1.0.0, or a commit SHA."
      SOURCE_REF="$2"; shift 2 ;;
    --source-dir)
      [[ $# -ge 2 ]] || fail "option_value_required" "--source-dir requires a directory." "Pass a dedicated local checkout path."
      SOURCE_INPUT="$2"; shift 2 ;;
    --skill)
      [[ $# -ge 2 ]] || fail "option_value_required" "--skill requires a Skill name." "Pass a lowercase published Skill name."
      [[ "$2" =~ ^[a-z0-9][a-z0-9._-]*$ ]] || fail "invalid_skill_name" "Invalid Skill name: $2" "Use the canonical lowercase Skill name shown by the source repository."
      SKILLS+=("$2"); shift 2 ;;
    --agent) OUTPUT_MODE="agent"; shift ;;
    --json) OUTPUT_MODE="json"; shift ;;
    --version) printf '%s\n' "$INSTALLER_VERSION"; exit 0 ;;
    -h|--help) usage; exit 0 ;;
    *) fail "unknown_option" "Unknown option: $1" "Run the installer with --help." ;;
  esac
done

command -v git >/dev/null 2>&1 || fail "missing_git" "Git is required." "Install Git and rerun the installer."
[[ -d "$PROJECT_INPUT" ]] || fail "project_missing" "Project directory does not exist: $PROJECT_INPUT" "Create the project directory, then rerun the installer."

PROJECT_DIR="$(cd "$PROJECT_INPUT" && pwd -P)"
SOURCE_PARENT="$(dirname "$SOURCE_INPUT")"
mkdir -p "$SOURCE_PARENT"
SOURCE_DIR="$SOURCE_INPUT"
LOG_FILE="$(mktemp)"
trap 'rm -f "$LOG_FILE"' EXIT

if [[ -e "$SOURCE_DIR" ]]; then
  [[ -d "$SOURCE_DIR/.git" ]] || fail "source_conflict" "Source path exists but is not a Git checkout: $SOURCE_DIR" "Choose an empty --source-dir or move the conflicting path."
  [[ -z "$(git -C "$SOURCE_DIR" status --porcelain)" ]] || fail "source_dirty" "Skill source has local changes: $SOURCE_DIR" "Commit, stash, or choose another --source-dir; the installer will not overwrite local work."
else
  run_logged "Git clone" git clone --recurse-submodules "$REPO_URL" "$SOURCE_DIR"
fi

run_logged "Git fetch" git -C "$SOURCE_DIR" fetch origin "$SOURCE_REF"
run_logged "Git checkout" git -C "$SOURCE_DIR" checkout --detach FETCH_HEAD
run_logged "Git submodule update" git -C "$SOURCE_DIR" submodule update --init --recursive
SOURCE_DIR="$(cd "$SOURCE_DIR" && pwd -P)"

MANAGER="$SOURCE_DIR/scripts/skills.sh"
[[ -x "$MANAGER" ]] || fail "manager_missing" "Portable Skill manager is missing: $MANAGER" "Use the yeisme-agent-my-skills repository or another compatible source checkout."

run_logged "Project initialization" "$MANAGER" --project "$PROJECT_DIR" init
for skill in "${SKILLS[@]}"; do
  run_logged "Skill activation: $skill" "$MANAGER" --project "$PROJECT_DIR" profile add "$skill"
done
if [[ "${#SKILLS[@]}" -gt 0 ]]; then
  run_logged "Skill synchronization" "$MANAGER" --project "$PROJECT_DIR" sync
fi
run_logged "Skill validation" "$MANAGER" --project "$PROJECT_DIR" validate

SOURCE_COMMIT="$(git -C "$SOURCE_DIR" rev-parse HEAD)"
render_success "$PROJECT_DIR" "$SOURCE_DIR" "$SOURCE_COMMIT"

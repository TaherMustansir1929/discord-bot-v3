#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# deploy.sh — Pull latest code, rebuild Docker image, restart container
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── Configuration (edit these) ───────────────────────────────────────────────
REPO_URL="https://github.com/TaherMustansir1929/discord-bot-v3.git"  # or SSH URL
REPO_DIR="./app"                     # where the repo lives (or will be cloned)
ENV_FILE=".env"                      # path to your .env file
BRANCH="main"                        # branch to pull from
# ─────────────────────────────────────────────────────────────────────────────

# ── Colours ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

log()     { echo -e "${CYAN}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*" >&2; }
step()    { echo -e "\n${BOLD}▶ $*${RESET}"; }
die()     { error "$*"; exit 1; }

# ── Preflight checks ──────────────────────────────────────────────────────────
step "Preflight checks"

command -v git    &>/dev/null || die "git is not installed."
command -v docker &>/dev/null || die "docker is not installed."

# Try without sudo first (user in docker group), fall back to sudo if needed
if docker info &>/dev/null; then
    DOCKER="docker"
elif sudo docker info &>/dev/null; then
    DOCKER="sudo docker"
else
    die "Docker daemon is not running (or permission denied). Try: sudo usermod -aG docker \$USER"
fi

log "Using Docker command: '${DOCKER}'"

[[ -f "$ENV_FILE" ]] || die ".env file not found at '$ENV_FILE'. Refusing to deploy without it."

success "All checks passed."

# ── Clone or pull ─────────────────────────────────────────────────────────────
step "Updating source code"

if [[ -d "$REPO_DIR/.git" ]]; then
    log "Repo found at '$REPO_DIR'. Pulling latest from '$BRANCH'..."
    git -C "$REPO_DIR" fetch origin
    git -C "$REPO_DIR" checkout "$BRANCH"
    BEFORE=$(git -C "$REPO_DIR" rev-parse HEAD)
    git -C "$REPO_DIR" reset --hard "origin/$BRANCH"
    AFTER=$(git -C "$REPO_DIR" rev-parse HEAD)

    if [[ "$BEFORE" == "$AFTER" ]]; then
        warn "No new commits since last deploy ($(git -C "$REPO_DIR" log -1 --format='%h %s'))."
        warn "Re-building image anyway..."
    else
        COMMITS=$(git -C "$REPO_DIR" log --oneline "${BEFORE}..${AFTER}")
        log "New commits:"
        echo "$COMMITS" | while IFS= read -r line; do echo "    $line"; done
    fi
else
    log "Repo not found. Cloning '$REPO_URL' into '$REPO_DIR'..."
    mkdir -p "$(dirname "$REPO_DIR")"
    git clone --branch "$BRANCH" --depth 1 "$REPO_URL" "$REPO_DIR"
fi

success "Source code is up to date."

# ── Self-Update Check ─────────────────────────────────────────────────────────
if [[ "$REPO_DIR" != "." && -f "$REPO_DIR/deploy.sh" ]]; then
    if ! cmp -s "$0" "$REPO_DIR/deploy.sh"; then
        warn "deploy.sh has been updated in the repository. Reloading script..."
        cp "$REPO_DIR/deploy.sh" "$0"
        exec bash "$0" "$@"
    fi
fi

# ── Build and Run with Docker Compose ─────────────────────────────────────────
step "Building and starting services"

# Resolve absolute path for ENV_FILE if it is a relative path
if [[ "$ENV_FILE" != /* ]]; then
    ENV_FILE_ABS="$(cd "$(dirname "$ENV_FILE")" && pwd)/$(basename "$ENV_FILE")"
else
    ENV_FILE_ABS="$ENV_FILE"
fi

cd "$REPO_DIR"
cp "$ENV_FILE_ABS" ./.env

$DOCKER compose --env-file .env up --build --detach

success "Services are running."

# ── Status summary ────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}── Deployment Summary ───────────────────────────────────────${RESET}"
echo -e "  Commit  : $(git -C "." log -1 --format='%h — %s (%cr)')"
echo -e "  Status  :"
$DOCKER compose ps
echo -e "${BOLD}─────────────────────────────────────────────────────────────${RESET}"
echo ""
echo -e "  ${CYAN}Logs:${RESET}     ${DOCKER} compose logs -f"
echo -e "  ${CYAN}Stop:${RESET}     ${DOCKER} compose down"
echo -e "  ${CYAN}Restart:${RESET}  ${DOCKER} compose restart"
echo ""

# ── Prune dangling images (optional cleanup) ──────────────────────────────────
DANGLING=$($DOCKER images -f "dangling=true" -q)
if [[ -n "$DANGLING" ]]; then
    log "Pruning $(echo "$DANGLING" | wc -l) dangling image(s) from previous builds..."
    $DOCKER image prune -f &>/dev/null
    success "Pruned dangling images."
fi
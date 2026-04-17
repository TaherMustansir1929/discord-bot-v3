#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# deploy.sh — Pull latest code, rebuild Docker image, restart container
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── Configuration (edit these) ───────────────────────────────────────────────
REPO_URL="https://github.com/TaherMustansir1929/discord-bot-v3.git"  # or SSH URL
REPO_DIR="./discord-bot"          # where the repo lives (or will be cloned)
IMAGE_NAME="discord-bot-v3"          # Docker image name
CONTAINER_NAME="discord-bot"         # Docker container name
ENV_FILE=".env"     # path to your .env file (outside repo)
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

# ── Build Docker image ────────────────────────────────────────────────────────
step "Building Docker image '$IMAGE_NAME'"

$DOCKER build \
    --tag  "${IMAGE_NAME}:latest" \
    --tag  "${IMAGE_NAME}:$(git -C "$REPO_DIR" rev-parse --short HEAD)" \
    --file "$REPO_DIR/Dockerfile" \
    "$REPO_DIR"

success "Image built: ${IMAGE_NAME}:latest"

# ── Stop & remove old container (if any) ─────────────────────────────────────
step "Replacing container '$CONTAINER_NAME'"

if $DOCKER ps -q --filter "name=^${CONTAINER_NAME}$" | grep -q .; then
    log "Stopping running container..."
    $DOCKER stop "$CONTAINER_NAME"
fi

if $DOCKER ps -aq --filter "name=^${CONTAINER_NAME}$" | grep -q .; then
    log "Removing old container..."
    $DOCKER rm "$CONTAINER_NAME"
fi

# ── Run new container ─────────────────────────────────────────────────────────
step "Starting container"

$DOCKER run \
    --detach \
    --name "$CONTAINER_NAME" \
    --env-file "$ENV_FILE" \
    --restart unless-stopped \
    "${IMAGE_NAME}:latest"

success "Container '${CONTAINER_NAME}' is running in detached mode."

# ── Status summary ────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}── Deployment Summary ───────────────────────────────────────${RESET}"
echo -e "  Commit  : $(git -C "$REPO_DIR" log -1 --format='%h — %s (%cr)')"
echo -e "  Image   : ${IMAGE_NAME}:latest"
echo -e "  Status  : $($DOCKER inspect -f '{{.State.Status}}' "$CONTAINER_NAME")"
echo -e "  Started : $($DOCKER inspect -f '{{.State.StartedAt}}' "$CONTAINER_NAME")"
echo -e "${BOLD}─────────────────────────────────────────────────────────────${RESET}"
echo ""
echo -e "  ${CYAN}Logs:${RESET}     ${DOCKER} logs -f ${CONTAINER_NAME}"
echo -e "  ${CYAN}Stop:${RESET}     ${DOCKER} stop ${CONTAINER_NAME}"
echo -e "  ${CYAN}Restart:${RESET}  ${DOCKER} restart ${CONTAINER_NAME}"
echo ""

# ── Prune dangling images (optional cleanup) ──────────────────────────────────
DANGLING=$($DOCKER images -f "dangling=true" -q)
if [[ -n "$DANGLING" ]]; then
    log "Pruning $(echo "$DANGLING" | wc -l) dangling image(s) from previous builds..."
    $DOCKER image prune -f &>/dev/null
    success "Pruned dangling images."
fi
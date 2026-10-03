#!/usr/bin/env bash
set -euo pipefail

# Create an isolated worktree + branch for one Story/role.
# Fails closed: the Story must exist and pass Definition of Ready.
#
# Usage: ./scripts/create-worktree.sh <story-id> <role> [base-branch]
# Example: ./scripts/create-worktree.sh US-101 backend

STORY_ID="${1:-}"
ROLE="${2:-}"
BASE="${3:-develop}"
WORKTREE_ROOT="${WORKTREE_ROOT:-/home/ubuntu/AI_Tutor-worktrees}"

usage() {
  echo "Usage: $0 <story-id> <role> [base-branch]"
  echo "Roles: backend | frontend | android | ios | tester | qa | devops"
  exit 1
}

[ -n "$STORY_ID" ] && [ -n "$ROLE" ] || usage

case "$ROLE" in
  backend)  SUFFIX="BE" ;;
  frontend) SUFFIX="FE" ;;
  android)  SUFFIX="Android" ;;
  ios)      SUFFIX="iOS" ;;
  tester|qa|devops) SUFFIX="$ROLE" ;;
  *) echo "Unknown role: $ROLE"; usage ;;
esac

if ! [[ "$STORY_ID" =~ ^US-[0-9]+$ ]]; then
  echo "Invalid story id: $STORY_ID (expected US-<number>)"
  exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

STORY_FILE="safe/stories/${STORY_ID}.yaml"
if ! STORY_FILE="$STORY_FILE" ./scripts/validate-story.sh; then
  echo "Story ${STORY_ID} is not READY. Worktree not created."
  exit 1
fi

if ! git rev-parse --verify --quiet "$BASE" >/dev/null; then
  echo "Base branch not found: $BASE"
  exit 1
fi

BRANCH="feature/${STORY_ID}-${ROLE}"
TARGET="${WORKTREE_ROOT}/${STORY_ID}-${SUFFIX}"

if git rev-parse --verify --quiet "$BRANCH" >/dev/null; then
  echo "Branch already exists: $BRANCH"
  exit 1
fi

if [ -e "$TARGET" ]; then
  echo "Worktree path already exists: $TARGET"
  exit 1
fi

mkdir -p "$WORKTREE_ROOT"
git worktree add "$TARGET" -b "$BRANCH" "$BASE"

echo "Worktree ready: $TARGET (branch $BRANCH from $BASE)"

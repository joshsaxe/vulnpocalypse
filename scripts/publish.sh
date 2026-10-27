#!/usr/bin/env bash
# Create a GitHub repository for this folder and push it.
#
#   bash scripts/publish.sh                    a PRIVATE repository called "vulnpocalypse" under your own account
#   bash scripts/publish.sh --public           make it public instead
#   bash scripts/publish.sh --name my-repo     use another repository name
#   bash scripts/publish.sh --owner my-org     create it under an organisation you belong to
#   bash scripts/publish.sh --as-me            first make the single commit yours (author = your git identity)
#   bash scripts/publish.sh --dry-run          say what would happen and change nothing
#
# Needs git and the GitHub CLI (https://cli.github.com), signed in with `gh auth login`.
# If this folder has no .git folder, the script makes one and a first commit.  The repository is private unless you
# pass --public; to change it later:  gh repo edit OWNER/NAME --visibility public --accept-visibility-change-consequences
set -euo pipefail

NAME="vulnpocalypse"
VISIBILITY="--private"
OWNER=""
AS_ME=0
DRY=0
DESCRIPTION='Data, code and annotated bibliography behind the post "If the vulnpocalypse is the apocalypse, where are the agentic attacker hordes?"'

while [[ $# -gt 0 ]]; do
  case "$1" in
    --public)  VISIBILITY="--public" ;;
    --private) VISIBILITY="--private" ;;
    --name)    NAME="${2:?--name needs a value}"; shift ;;
    --owner)   OWNER="${2:?--owner needs a value}"; shift ;;
    --as-me)   AS_ME=1 ;;
    --dry-run) DRY=1 ;;
    -h|--help) sed -n '2,13p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1 (try --help)" >&2; exit 2 ;;
  esac
  shift
done

say() { printf '==> %s\n' "$*"; }
run() {
  if [[ "$DRY" == 1 ]]; then printf '[dry run] %s\n' "$*"; else "$@"; fi
}

cd "$(dirname "${BASH_SOURCE[0]}")/.."

command -v git >/dev/null || { echo "git is not installed" >&2; exit 1; }
command -v gh  >/dev/null || { echo "the GitHub CLI (gh) is not installed: https://cli.github.com" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh is not signed in: run 'gh auth login' first" >&2; exit 1; }

[[ -n "$OWNER" ]] || OWNER="$(gh api user --jq .login)"
FULL="$OWNER/$NAME"
WORD="private"; [[ "$VISIBILITY" == "--public" ]] && WORD="public"

# 1. A git repository with everything committed.
if [[ ! -d .git ]]; then
  say "no .git folder here: creating a repository and a first commit"
  run git init -q -b main
  run git add -A
  run git commit -q -m "Add data, code and annotated bibliography for the vulnpocalypse post"
elif [[ -n "$(git status --porcelain)" ]]; then
  echo "this folder has uncommitted changes; commit or stash them first (git status shows them)" >&2
  exit 1
fi

if [[ "$AS_ME" == 1 ]]; then
  if [[ "$(git rev-list --count HEAD 2>/dev/null || echo 0)" != 1 ]]; then
    echo "--as-me only works when the history is a single commit" >&2
    exit 1
  fi
  say "making the commit yours (if you sign commits, it is signed again with your key)"
  run git commit -q --amend --reset-author --no-edit
fi

# 2. The GitHub repository, and the push.
if git remote get-url origin >/dev/null 2>&1; then
  say "a remote called origin already exists ($(git remote get-url origin)): pushing to it"
  run git push -u origin HEAD
else
  if gh repo view "$FULL" >/dev/null 2>&1; then
    echo "$FULL already exists on GitHub, so it was not created. To push to it anyway:" >&2
    echo "  git remote add origin https://github.com/$FULL.git && git push -u origin HEAD" >&2
    exit 1
  fi
  say "creating the $WORD repository $FULL and pushing"
  run gh repo create "$FULL" "$VISIBILITY" --description "$DESCRIPTION" --source=. --remote=origin --push
  run gh repo edit "$FULL" --add-topic cybersecurity --add-topic artificial-intelligence \
      --add-topic bayesian-inference --add-topic reproducible-research --add-topic data-visualization || true
fi

say "done: https://github.com/$FULL ($WORD)"
if [[ "$WORD" == "private" ]]; then
  say "to make it public when the post is out:  gh repo edit $FULL --visibility public --accept-visibility-change-consequences"
fi
say "then add the address to CITATION.cff as  repository-code: https://github.com/$FULL"

#!/usr/bin/env bash
# Install the repository's git hooks (.githooks/) for this clone.
#
# If you already use a global core.hooksPath (for example a dispatcher that
# chains to .git/hooks), the hooks are linked into .git/hooks so your global
# hooks keep running. Otherwise core.hooksPath is pointed at .githooks.
set -euo pipefail
root=$(git rev-parse --show-toplevel)
cd "$root"
chmod +x .githooks/* scripts/check_docs.py scripts/ai_review.py

if [ -n "$(git config --global --get core.hooksPath || true)" ]; then
  hooks_dir=$(git rev-parse --git-path hooks)
  mkdir -p "$hooks_dir"
  for hook in .githooks/*; do
    name=$(basename "$hook")
    ln -sf "$root/$hook" "$hooks_dir/$name"
    echo "linked $hooks_dir/$name -> $hook"
  done
  echo "Global core.hooksPath detected: make sure it chains to .git/hooks."
else
  git config core.hooksPath .githooks
  echo "core.hooksPath set to .githooks"
fi

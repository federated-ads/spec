#!/usr/bin/env bash
# Install the repository's git hooks for this clone.
#
# The hooks are COPIED into the clone's .git/hooks, not linked, and they run
# the checks from the trusted ref origin/main. A branch you check out cannot
# change what runs. Re-run this script after the hooks change on main.
#
# If you use a global core.hooksPath, make sure it chains to .git/hooks.
# Otherwise core.hooksPath is pointed at .git/hooks for this clone.
set -euo pipefail
root=$(git rev-parse --show-toplevel)
cd "$root"
# Always the clone's own hooks directory. (git rev-parse --git-path hooks
# would follow a global core.hooksPath and overwrite shared hooks.)
hooks_dir="$(git rev-parse --absolute-git-dir)/hooks"
mkdir -p "$hooks_dir"

install -m 0644 .githooks/lib.sh "$hooks_dir/federated-ads-hooks-lib.sh"
for name in pre-commit pre-push; do
  rm -f "$hooks_dir/$name"
  install -m 0755 ".githooks/$name" "$hooks_dir/$name"
  echo "installed $hooks_dir/$name"
done

if [ -z "$(git config --global --get core.hooksPath || true)" ]; then
  echo "No global core.hooksPath: git uses .git/hooks directly."
else
  echo "Global core.hooksPath detected: make sure it chains to .git/hooks."
fi

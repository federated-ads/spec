#!/usr/bin/env bash
# Install the repository's git hooks for this clone.
#
# The hooks are COPIED into the repository's hooks directory, not linked, and
# they run the checks from the trusted ref origin/main, so a branch you check
# out cannot change what runs. Re-run this script after the hooks change on
# main. Existing hooks that this script did not install are backed up first.
#
# If core.hooksPath is set (at any level) git reads hooks from there instead;
# make sure whatever lives there chains to the repository's hooks directory.
set -euo pipefail
root=$(git rev-parse --show-toplevel)
cd "$root"

# The common git dir, so linked worktrees install where git reads hooks.
# (git rev-parse --git-path hooks would follow core.hooksPath and could
# overwrite shared global hooks.)
common_dir=$(cd "$(git rev-parse --git-common-dir)" && pwd)
hooks_dir="$common_dir/hooks"
mkdir -p "$hooks_dir"
marker="Federated Ads editorial hooks"

install -m 0644 .githooks/lib.sh "$hooks_dir/federated-ads-hooks-lib.sh"
for name in pre-commit pre-push; do
  target="$hooks_dir/$name"
  if [ -e "$target" ] && ! grep -q "$marker" "$target" 2>/dev/null; then
    backup="$target.backup.$(date +%Y%m%d%H%M%S)"
    mv "$target" "$backup"
    echo "backed up existing $name hook to $backup"
  fi
  rm -f "$target"
  install -m 0755 ".githooks/$name" "$target"
  echo "installed $target"
done

hooks_path=$(git config --get core.hooksPath || true)
if [ -n "$hooks_path" ]; then
  echo "core.hooksPath is set to $hooks_path: make sure it chains to $hooks_dir."
fi

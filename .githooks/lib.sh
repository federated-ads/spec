# Shared by the installed hooks. Copied into .git/hooks at install time.
#
# The checks run from a trusted, reviewed ref (origin/main by default), not
# from the working tree, so checking out an untrusted branch cannot change
# what executes on your machine. While developing the checks themselves, set
# FA_HOOKS_TRUST_WORKTREE=1 to run the working-tree copies instead.
#
# python3 -I (isolated mode) keeps the working tree off sys.path, so a branch
# cannot shadow standard-library modules the trusted script imports.

TRUSTED_REF=${FA_HOOKS_TRUSTED_REF:-origin/main}

run_trusted() {
  local script=$1; shift
  local root src
  root=$(git rev-parse --show-toplevel)
  if [ "${FA_HOOKS_TRUST_WORKTREE:-0}" = "1" ]; then
    python3 -I "$root/$script" "$@"
    return
  fi
  if ! src=$(git show "$TRUSTED_REF:$script" 2>/dev/null); then
    echo "hooks: $script is not on $TRUSTED_REF yet; skipped" \
         "(set FA_HOOKS_TRUST_WORKTREE=1 to run the local copy)" >&2
    return 0
  fi
  (cd "$root" && python3 -I - "$@" <<<"$src")
}

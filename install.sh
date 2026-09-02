#!/usr/bin/env sh
# Install coba for iTerm2: dynamic profiles plus side padding.
set -eu

# The cp sources below are relative, so anchor to the repo rather than to cwd.
cd -- "$(dirname -- "$0")"

# Not pgrep: it does not report the calling process's own ancestors, and this
# script is normally run from inside iTerm2, so pgrep never sees it. That is
# exactly what SC2009 recommends, and it is wrong here.
# shellcheck disable=SC2009
if ps -Ao comm= 2>/dev/null | grep -q 'iTerm\.app/Contents/MacOS/iTerm2'; then
  echo "quit iTerm2 first: it rewrites its plist on exit and will clobber the margins" >&2
  exit 1
fi

DP="$HOME/Library/Application Support/iTerm2/DynamicProfiles"
CFG="$HOME/.config/iterm2"
mkdir -p "$DP" "$CFG"

# The four settings below are app-wide and have no uninstall. Record what they
# were, once, so there is something to put back.
BEFORE="$CFG/coba-pre-install.txt"
if [ ! -f "$BEFORE" ]; then
  for k in SideMargins TopBottomMargins extendBackgroundColorIntoMargins \
           "Default Bookmark Guid"; do
    printf '%s=%s\n' "$k" \
      "$(defaults read com.googlecode.iterm2 "$k" 2>/dev/null || echo '<unset>')"
  done > "$BEFORE"
  echo "saved previous iTerm2 settings to $BEFORE"
fi

cp iterm/coba.json "$DP/coba.json"
cp iterm/coba-wax.itermcolors iterm/coba-pine.itermcolors \
   iterm/coba-dawn.itermcolors iterm/coba-dusk.itermcolors "$CFG/"

# iTerm has no per-profile margin: these are app-wide (Settings > Appearance > Panes).
defaults write com.googlecode.iterm2 SideMargins -int 24
defaults write com.googlecode.iterm2 TopBottomMargins -int 14
# Paint the margins in the session background so the padding reads as padding.
defaults write com.googlecode.iterm2 extendBackgroundColorIntoMargins -bool true

defaults write com.googlecode.iterm2 "Default Bookmark Guid" "1A0DEE71-1E00-4B0A-9E51-1B0EC1F0A1DE"

echo "installed. coba is now the default iTerm2 profile."

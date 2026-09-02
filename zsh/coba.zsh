# coba for zsh: autosuggestions + syntax highlighting.
#
# Every colour here is an ANSI index, not a hex value, on purpose. iTerm
# resolves 0-15 through whichever coba profile is active, so the highlighting
# follows the macOS light/dark switch for free. Hard-coding hex would pin it
# to one ground and look wrong in the other.
#
#   1 red   2 green   3 yellow/ocre   4 blue   5 rose   6 teal   8 dim
# Wax resolves those to Salubra earths, pine to greens, dusk and dawn to the
# slate pair. All four hold the same floors, so this file needs no edit.

_coba_plugin() {
  local f="/opt/homebrew/share/$1/$1.zsh"
  [[ ! -r $f ]] || source "$f"
}

# --- pure prompt ----------------------------------------------------------
# Pure hardcodes five of its slots to xterm-256 indices rather than ANSI 0-15,
# so coba never reaches them and they render the same grey on every ground:
# 242 (#6c6c6c) falls to 2.6:1 on pine and 3.4:1 on dusk, and 218 (#ffafd7),
# its dirty marker, is 1.5:1 on light. Point them at the palette instead.
zstyle ':prompt:pure:virtualenv'          color 8
zstyle ':prompt:pure:git:branch'          color 8
zstyle ':prompt:pure:host'                color 8
zstyle ':prompt:pure:user'                color 8
zstyle ':prompt:pure:prompt:continuation' color 8
zstyle ':prompt:pure:git:dirty'           color 3

# --- autosuggestions ------------------------------------------------------
# 8 is the dim slot in all four variants (ombre naturelle moyenne in wax, a
# dimmed green in pine, slate grey in dusk and dawn), and the one build.py
# holds to a 3:1 floor against whichever ground is active.
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=8'
ZSH_AUTOSUGGEST_STRATEGY=(history completion)
_coba_plugin zsh-autosuggestions

# --- syntax highlighting --------------------------------------------------
# Must come after autosuggestions: it wraps the ZLE widgets and wants to be last.
ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets)

typeset -gA ZSH_HIGHLIGHT_STYLES
ZSH_HIGHLIGHT_STYLES[unknown-token]='fg=1,bold'
ZSH_HIGHLIGHT_STYLES[reserved-word]='fg=5'
ZSH_HIGHLIGHT_STYLES[alias]='fg=2'
ZSH_HIGHLIGHT_STYLES[builtin]='fg=2'
ZSH_HIGHLIGHT_STYLES[function]='fg=2'
ZSH_HIGHLIGHT_STYLES[command]='fg=2'
ZSH_HIGHLIGHT_STYLES[precommand]='fg=2,underline'
ZSH_HIGHLIGHT_STYLES[commandseparator]='fg=5'
ZSH_HIGHLIGHT_STYLES[hashed-command]='fg=2'
ZSH_HIGHLIGHT_STYLES[path]='fg=4'
ZSH_HIGHLIGHT_STYLES[path_prefix]='fg=4'
ZSH_HIGHLIGHT_STYLES[globbing]='fg=3'
ZSH_HIGHLIGHT_STYLES[history-expansion]='fg=5'
ZSH_HIGHLIGHT_STYLES[single-hyphen-option]='fg=6'
ZSH_HIGHLIGHT_STYLES[double-hyphen-option]='fg=6'
ZSH_HIGHLIGHT_STYLES[back-quoted-argument]='fg=6'
ZSH_HIGHLIGHT_STYLES[single-quoted-argument]='fg=3'
ZSH_HIGHLIGHT_STYLES[double-quoted-argument]='fg=3'
ZSH_HIGHLIGHT_STYLES[dollar-quoted-argument]='fg=3'
ZSH_HIGHLIGHT_STYLES[dollar-double-quoted-argument]='fg=6'
ZSH_HIGHLIGHT_STYLES[back-double-quoted-argument]='fg=6'
ZSH_HIGHLIGHT_STYLES[assign]='fg=4'
ZSH_HIGHLIGHT_STYLES[redirection]='fg=5'
ZSH_HIGHLIGHT_STYLES[comment]='fg=8'
ZSH_HIGHLIGHT_STYLES[named-fd]='fg=6'
ZSH_HIGHLIGHT_STYLES[arg0]='fg=2'
ZSH_HIGHLIGHT_STYLES[default]='none'
ZSH_HIGHLIGHT_STYLES[bracket-error]='fg=1,bold'
for i in 1 2 3 4 5; do
  ZSH_HIGHLIGHT_STYLES[bracket-level-$i]="fg=$(( (i % 5) + 2 ))"
done
unset i

_coba_plugin zsh-syntax-highlighting
unset -f _coba_plugin

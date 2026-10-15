#!/usr/bin/env bash
# Render a Mermaid or SVG source to PNG for the visualize makers.
#
#   .claude/tools/render.sh mermaid|svg <source> <out.png>             # preview
#   .claude/tools/render.sh mermaid|svg <source> --publish <slug>       # publish into the vault's viz/
#
# --publish writes <vault>/viz/viz-<slug>-<timestamp>.png and prints "filename:" and "path:".
# Mermaid uses the local mermaid-cli with the system Chromium; SVG uses rsvg-convert,
# falling back to ImageMagick.
set -euo pipefail

TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIZ="$HOME/Documents/AI Engineering/viz"
kind="${1:-}"; src="${2:-}"; shift 2 || true

[[ "$kind" == mermaid || "$kind" == svg ]] || { echo "usage: render.sh mermaid|svg <source> <out.png> | --publish <slug>" >&2; exit 2; }
[[ -f "$src" ]] || { echo "source not found: $src" >&2; exit 2; }

if [[ "${1:-}" == "--publish" ]]; then
  slug="$(printf '%s' "${2:-diagram}" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]\+/-/g; s/^-//; s/-$//')"
  mkdir -p "$VIZ"
  out="$VIZ/viz-${slug:-diagram}-$(date +%Y%m%d-%H%M%S).png"
else
  out="${1:?missing output path}"
fi

case "$kind" in
  mermaid)
    "$TOOLS/node_modules/.bin/mmdc" -q -p "$TOOLS/puppeteer.json" -b white -s 2 -i "$src" -o "$out" ;;
  svg)
    if command -v rsvg-convert >/dev/null && rsvg-convert -z 2 -b white "$src" -o "$out" 2>/dev/null; then :
    else magick -density 192 -background white "$src" "$out"; fi ;;
esac

[[ -s "$out" ]] || { echo "render failed: no output" >&2; exit 1; }
if [[ "${1:-}" == "--publish" ]]; then
  echo "filename: $(basename "$out")"
  echo "path: $out"
else
  echo "rendered: $out"
fi

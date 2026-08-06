#!/usr/bin/env bash
# Render markdown sources to PDF via pandoc + typst.
#
# Usage:
#   render_pdfs.sh <application_dir>
#
# Renders <application_dir>/cv.md -> cv.pdf
#         <application_dir>/cover_letter.md -> cover_letter.pdf
#
# Errors are non-fatal: if cv.md is missing, skips; if pandoc/typst missing, warns.

set -u

APP_DIR="${1:-}"
if [[ -z "$APP_DIR" ]]; then
  echo "Usage: render_pdfs.sh <application_dir>" >&2
  exit 1
fi

if [[ ! -d "$APP_DIR" ]]; then
  echo "Error: directory does not exist: $APP_DIR" >&2
  exit 1
fi

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc not installed. Run: brew install pandoc" >&2
  exit 1
fi

if ! command -v typst >/dev/null 2>&1; then
  echo "Error: typst not installed. Run: brew install typst" >&2
  exit 1
fi

TEMPLATE_DIR="$(cd "$(dirname "$0")/.." && pwd)/templates/pandoc"
# Note: for v1 we use pandoc's default typst template; the custom template at
# $TEMPLATE_DIR/minimal.typ is a v2 styling hook.

render() {
  local src="$1"
  local out="$2"
  if [[ ! -f "$src" ]]; then
    return 0
  fi
  echo "Rendering $src -> $out"
  if pandoc "$src" -o "$out" \
      --pdf-engine=typst \
      -V geometry:margin=0.75in \
      -V fontsize:10.5pt \
      -V mainfont="Helvetica Neue" \
      2>"$src.render.err"; then
    rm -f "$src.render.err"
    echo "  OK"
  else
    echo "  FAILED — see $src.render.err"
  fi
}

render "$APP_DIR/cv.md" "$APP_DIR/cv.pdf"
render "$APP_DIR/cover_letter.md" "$APP_DIR/cover_letter.pdf"

echo "Done."

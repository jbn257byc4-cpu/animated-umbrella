#!/bin/sh
# Renders flyer/index.html to flyer/flyer.png (1080x1920) with headless Chromium.
# Usage: ./render.sh [path-to-chromium]
CHROME="${1:-chromium}"
cd "$(dirname "$0")" || exit 1
"$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --screenshot=flyer.png --window-size=1080,1920 "file://$PWD/index.html"

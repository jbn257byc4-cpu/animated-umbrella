#!/bin/sh
# Renders flyer/index.html to flyer/flyer.png (1080x1920) with headless Chromium.
# Usage: ./render.sh [path-to-chromium]
set -e
CHROME="${1:-chromium}"
cd "$(dirname "$0")"

WIDTH=1080
HEIGHT=1920
# Headless Chromium hands part of --window-size to window chrome, so a capture
# at exactly $HEIGHT loses its last rows. Grab a taller window, then trim.
SLACK=240

"$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 \
  --virtual-time-budget=6000 \
  --screenshot=flyer.png \
  --window-size="$WIDTH,$((HEIGHT + SLACK))" \
  "file://$PWD/index.html"

python3 crop_png.py flyer.png "$HEIGHT"

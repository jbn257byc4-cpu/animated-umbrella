#!/bin/sh
CHROME="${1:-chromium}"
cd "$(dirname "$0")" || exit 1
"$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --screenshot=flyer.png --window-size=1080,1350 "file://$PWD/index.html"

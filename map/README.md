# Swartland Water Routes

An interactive 3D schematic of how bulk water reaches Darling and Yzerfontein:
the existing route from the Berg River catchment through Voëlvlei Dam and the
WCDM bulk system, plus the planned BRVAS augmentation.

`index.html` is a single self-contained file — fonts are embedded as data URIs
and there are no external requests. Open it directly in a browser.

## How it works

The terrain and the schematic share one oblique camera (`P(x, y, z)`), so the
lit heightfield drawn to `<canvas>` and the pipes, tanks and buildings drawn to
the `<svg>` overlay sit in the same 3D space. Structures are built from real
box and cylinder geometry with back-face culling; pipes are sampled onto the
ground surface so they follow the landscape.

## Routes are links

Every route and asset is an `<a href="#route=…">` or `<a href="#asset=…">`, and
the URL hash is the single source of truth for selection. That makes each route
shareable, keyboard-navigable and back-button friendly:

    index.html#route=bulk
    index.html#asset=glen-lilly

## Editing the network

`NODES` and `ROUTES` near the bottom of the script hold the whole diagram.
Node coordinates are world units (x 0–760 east–west, y 0–1400 north–south);
elevation is looked up from the terrain automatically.

## Rendering a still

    /opt/pw-browsers/chromium --headless --screenshot=map.png \
      --window-size=1480,1470 "file://$PWD/index.html"

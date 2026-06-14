# No410

> **The one and only in the city.**

A single-page marketing site for **No410** — a double-storey detached residence at Jalan Hilltop Utama, Miri, Sarawak. Built as a cinematic, motion-driven website with the full architectural set: photoreal renders, design studies, all four elevations, both floor plans, a styled location map with drive times, and an animated hero background.

— Developed by **Sunhouri Property Holdings Sdn Bhd**
— Authorised Marketing Agency: **Elite Estate Group**

---

## Quick start

The site is plain HTML/CSS/JS — no build step, no dependencies.

```bash
# clone
git clone https://github.com/<you>/no410.git
cd no410

# preview locally (any static server works)
python3 -m http.server 8080
# then open http://localhost:8080
```

Just opening `index.html` directly in the browser also works, though some browsers restrict `file://` for autoplay and certain features. A local server is recommended.

## Project structure

```
no410/
├── index.html                 # markup
├── assets/
│   ├── style.css              # all styling (Fraunces + JetBrains Mono, ivory/bronze palette)
│   ├── main.js                # motion, parallax, plan tabs, video loader
│   ├── images/                # renders, elevations, plans, design studies, logo
│   └── video/
│       ├── hero.mp4           # H.264 hero background (~700 KB)
│       ├── hero.webm          # VP9 fallback (~550 KB)
│       └── hero_poster.jpg    # first frame, used as poster + no-autoplay fallback
├── scripts/
│   └── build_bundle.py        # bundles everything into a single self-contained HTML
├── docs/
│   ├── CONTENT.md             # copy & spec inventory (edit content here, then update index.html)
│   └── CHANGELOG.md
├── LICENSE
└── README.md
```

## Editing

| To change... | Edit... |
|---|---|
| Copy / wording | `index.html` (and mirror in `docs/CONTENT.md`) |
| Colours, type, spacing | `assets/style.css` (CSS custom properties at the top) |
| Animation timing, plan tabs, parallax | `assets/main.js` |
| Photos | replace files in `assets/images/`, keep filenames |
| Hero video | replace `hero.mp4` + `hero.webm` + `hero_poster.jpg` |
| Location map | `index.html` → `<svg class="sitemap">` (hand-drawn SVG) |
| Drive times | `index.html` → `<ul class="drives">` |
| Floor-plan legends | `index.html` → `<ul class="rooms">` inside each `.panel` |

## Build the single-file bundle

For sharing the brochure as one HTML file (email, WhatsApp, Drive), inline everything:

```bash
python3 scripts/build_bundle.py
# outputs dist/no410_bundle.html (~7-9 MB, single file)
```

## Design system

- **Palette** — ink `#15161a`, ivory `#f3f1ec`, paper `#e9e7e1`, bronze `#9a6a3c` (single accent)
- **Type** — Fraunces (high-contrast serif, display) + Space Grotesk (body) + JetBrains Mono (labels/specs)
- **Motion** — slow cinematic easing `cubic-bezier(.16,1,.3,1)`, parallax on bleed images, animated hero video, count-up stats, word-by-word reveals
- **Architectural motif** — the `410` plaque, technical-drawing frame (datum labels top/bottom), dimension ticks on the location map, corner registration marks on the plan figure

## Property details

- **Address** — Lot 410, Block 10, M.C.L.D., Jalan Hilltop Utama, Miri, Sarawak
- **Coordinates** — 4°22′33″N 113°59′11″E
- **Type** — Double-storey detached residence
- **Built-up** — 3,406.77 sq ft
- **Land size** — 19 points
- **Bedrooms / Bathrooms** — 4 / 5
- **Car porch** — 3-car
- **Estimated completion** — End 2026
- **Selling price** — RM 3,380,000

See `docs/CONTENT.md` for the full content inventory.

## Credits

- **Developer** — Sunhouri Property Holdings Sdn Bhd
- **Architect** — James Sie & Associate, Miri
- **Authorised Marketing Agency** — Elite Estate Group

## License

Code is MIT licensed (see `LICENSE`). All renders, plans, elevations, the developer/agency marks, and the project name **No410** remain the property of their respective owners and are used here for marketing purposes only.

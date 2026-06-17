# US Road Trip Explorer

A mobile-first progressive web app for family road trips across the United States. Map LDS temples and major four-year universities, track which sites you've visited, and navigate to any location with a single tap.

Built as a zero-build, single-file web application — no Node.js compilation step required.

## Features

### Current

- Full-screen interactive map centered on the continental US
- OpenStreetMap tiles via [Leaflet.js](https://leafletjs.com/)
- [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster) wired up for high-performance rendering of hundreds of markers
- Mobile-optimized viewport with double-click / double-tap zoom
- Floating semi-transparent header bar with master progress bar (`X / Y Sites Visited • Z%`)
- **`universities.json`** — 456 major US four-year universities (NCAA Division I + prominent regional institutions) across all 50 states and DC, with campus coordinates
- Async dual-source data loading via `Promise.all` (`universities.json` + temple KML)
- KML parsing with native `DOMParser()` — US temples filtered and normalized at runtime
- Gold temple pins and deep blue university pins on a shared marker cluster (~655 locations)
- Marker popups with location details, native Google Maps **Navigate** deep link, and **Mark as Visited** toggle
- Visited markers fade to light gray at 35% opacity; cluster appearance refreshes instantly
- Slide-up checklist drawer (FAB toggle) with state accordions and Temples/Universities tabs
- Two-way sync between map popups and checklist checkboxes
- Offline progress persistence via `localStorage` keyed by each location's unique ID

### Planned

- Filter/hide visited markers from viewport (optional view mode)
- Search or jump-to-state shortcuts in the checklist drawer

See [project_spec.md](project_spec.md) for the full specification.

## Tech Stack

- HTML5, ES6+ JavaScript
- [Tailwind CSS](https://tailwindcss.com/) (CDN)
- [Leaflet.js](https://leafletjs.com/) 1.9.4 (CDN)
- [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster) 1.5.3 (CDN)

## Getting Started

Clone the repository and serve the files with any static HTTP server:

```bash
git clone https://github.com/jrdespai/roadtrip_tracker.git
cd roadtrip_tracker
python3 -m http.server 8765
```

Open [http://localhost:8765](http://localhost:8765) in your browser. For the best experience, use a mobile device or your browser's device emulation mode.

## Project Structure

```
roadtrip_tracker/
├── index.html                              # Application shell and map logic
├── project_spec.md                         # Full feature specification
├── universities.json                       # US university database (456 entries)
├── scripts/build_universities.py           # Regenerates universities.json from public sources
└── ChurchofJesusChristTemples (1).kml      # Global temple KML source (US entries parsed at runtime)
```

## Active Sprint

**Current:** Sprint complete — checklist drawer, visited-state tracking, popups, and `localStorage` persistence are live. Next up: optional visited-marker filtering and checklist search/navigation enhancements.

## Changelog

### 2026-06-16 — Checklist drawer & progress tracking sprint (complete)

- [x] Master progress bar in header showing visited count and percentage
- [x] Floating action button (list icon) toggles slide-up checklist drawer
- [x] State accordion layout grouping all locations by US state
- [x] Temples / Universities tabs within each state, sorted alphabetically
- [x] Large touch-friendly checkboxes (44px min tap targets) in drawer and popups
- [x] Two-way sync: checklist checkboxes ↔ map popup "Mark as Visited" toggle
- [x] `localStorage` persistence keyed by location ID survives page reloads
- [x] Visited markers switch to faded gray (35% opacity) with cluster refresh
- [x] Strikethrough styling on visited items in the checklist drawer
- [x] Marker popups with Navigate CTA (`maps.google.com/?q=lat,lng` deep link)

### 2026-06-16 — Data loading & map markers sprint (complete)

- [x] Load `universities.json` and `ChurchofJesusChristTemples (1).kml` concurrently with `Promise.all`
- [x] Parse KML `<Placemark>` entries via `DOMParser()`, extract name/coordinates/description
- [x] Filter to US temples only; normalize to unified location schema
- [x] Merge universities + temples into one in-memory list
- [x] Render gold temple pins and deep blue university pins on `L.markerClusterGroup()`

### 2026-06-16 — University data sprint (complete)

- [x] Populate `universities.json` with 456 major four-year universities nationwide
- [x] Include all NCAA Division I institutions (357) plus prominent regional supplements (Alaska system, Ivy/LAC schools, flagship branch campuses)
- [x] Normalize schema: `id`, `name`, `type`, `city`, `state`, `lat`, `lng`
- [x] Add `scripts/build_universities.py` to regenerate the dataset from [d1-atlas](https://github.com/Lowgy/d1-atlas) and [us-colleges](https://github.com/zicodeng/us-colleges) sources

## License

Personal project — no license specified yet.

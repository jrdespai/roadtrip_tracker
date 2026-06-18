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
- Marker popups with location details, native Google Maps **Navigate** deep link (`google.com/maps/search/?api=1`), and **Mark as Visited** toggle
- Visited markers fade to light gray at 35% opacity; cluster appearance refreshes instantly
- **Hide Visited** floating toggle removes visited markers from the map cluster for a cleaner road-ahead view
- Slide-up checklist drawer (FAB toggle) with state accordions, Temples/Universities tabs, and per-location **Navigate** buttons
- Two-way sync between map popups and checklist checkboxes
- Offline progress persistence via `localStorage` keyed by each location's unique ID
- 44×44px minimum touch targets on all buttons, checkboxes, tabs, and accordion headers

### Planned

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

**Current:** Road trip tools sprint complete — native Google Maps navigation, Hide Visited map filter, and 44px touch targets are live. Next up: checklist search and jump-to-state shortcuts.

## Changelog

### 2026-06-16 — Navigate button contrast fix

- [x] Force white text on popup and checklist **Navigate** buttons (overrides Leaflet link color)

### 2026-06-16 — Road trip tools & touch targets sprint (complete)

- [x] **Navigate** buttons in map popups and checklist rows open native Google Maps via `https://www.google.com/maps/search/?api=1&query={lat},{lng}`
- [x] Floating **Hide Visited** toggle at top of map removes visited markers from the cluster group
- [x] Visited/unvisited changes sync instantly with Hide Visited filter (markers appear or disappear on toggle)
- [x] 44×44px minimum tap targets on Navigate buttons, checkboxes, tabs, accordion headers, FAB, and drawer close

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
- [x] Marker popups with Navigate CTA (Google Maps native deep link)

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

# US Road Trip Explorer

A mobile-first progressive web app for family road trips across the United States. Map LDS temples and major four-year universities, track which sites you've visited, and navigate to any location with a single tap.

Built as a zero-build, single-file web application — no Node.js compilation step required.

## Features

### Current

- Full-screen interactive map centered on the continental US
- OpenStreetMap tiles via [Leaflet.js](https://leafletjs.com/)
- [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster) wired up for high-performance rendering of hundreds of markers
- Mobile-optimized viewport with double-click / double-tap zoom
- Floating semi-transparent header bar
- **`universities.json`** — 456 major US four-year universities (NCAA Division I + prominent regional institutions) across all 50 states and DC, with campus coordinates
- Async dual-source data loading via `Promise.all` (`universities.json` + temple KML)
- KML parsing with native `DOMParser()` — US temples filtered and normalized at runtime
- Gold temple pins and deep blue university pins on a shared marker cluster (~655 locations)

### Planned

- Marker popups with Navigate and Mark as Visited actions
- Visited-state marker styling
- Slide-up checklist drawer grouped by state and type
- Offline progress persistence via `localStorage`
- Native Google Maps deep-link navigation

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

**Current:** Add marker popups with Navigate and Mark as Visited actions, plus visited-state styling and `localStorage` persistence.

## Changelog

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

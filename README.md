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

### Planned

- Temple and university markers parsed from static KML and JSON data files
- Gold temple pins and blue university pins with visited-state styling
- Marker popups with Navigate and Mark as Visited actions
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
├── universities.json                       # (planned) US university database
└── ChurchofJesusChristTemples (1).kml      # (planned) Global temple KML source
```

## License

Personal project — no license specified yet.

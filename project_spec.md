# Project Specification: US Road Trip Site Explorer

## 1. Overview & Purpose

A mobile-optimized, single-page progressive web application designed for family road trips. The application maps out all operating, announced, and under-construction temples of the Church of Jesus Christ of Latter-day Saints alongside major four-year universities in the United States. Users can track their progress by checking off visited sites via the map or an integrated state-by-state checklist drawer.

## 2. Target Audience & UX Goals

- Primary Platform: Mobile Web (Safari/Chrome on iOS & Android).

- Environment: Moving vehicle (requires high contrast, large 44x44px minimal tap targets, and resilient offline-first data retention).

- Core Requirement: High-performance mapping that can comfortably display 600+ complex marker points simultaneously on low-tier mobile devices without interface lagging.

## 3. Technology Stack & Architecture

To maintain maximum deployment simplicity and speed, the application operates strictly as a zero-compilation, single-file client web application paired with static data assets.

- Frontend Interface: HTML5, native ES6+ JavaScript, Tailwind CSS via CDN.

- Mapping Engine: Leaflet.js (OpenStreetMap tile rendering engine) via CDN.

- Performance Clustering: Leaflet.markercluster plugin via CDN.

- Data Ingestion: Native browser DOMParser() to consume and strip raw KML node streams without external Node.js build steps.

## 4. Data Layer & Assets

The workspace directory must be structured exactly as follows:

[Workspace Folder]

  |-- index.html                           # Single-file core application logic & UI

  |-- universities.json                     # Static JSON database of US universities 

  |-- ChurchofJesusChristTemples (1).kml    # Raw XML/KML database of global temples

### Data Normalization Schema (In-Memory Array)

Regardless of the original source format, all locations must be mapped into a unified JavaScript object layout at runtime:

{

  "id": "string (e.g., 'temple-12' or 'uni-asu')",

  "name": "string",

  "type": "temple" | "university",

  "city": "string",

  "state": "string (2-Letter uppercase)",

  "lat": "float (decimal degrees)",

  "lng": "float (decimal degrees)"

}

## 5. Feature Requirements & Logic Boundaries

### A. Data Ingestion & Pruning Filters

1. KML Parsing Boundary: Read ChurchofJesusChristTemples (1).kml. The logic must extract the <name> element, the <coordinates> tag (lng,lat,alt sequence), and parse out the location text inside the HTML <description> tag.

2. Geographic Scoping: Automatically discard international temples during parsing. If the <description> metadata does not explicitly contain "United States", or the extracted coordinates fall outside US bounds, omit the entry.

### B. Map Interaction & Custom Clustering

1. Marker Styling:

   - Active State: Temples must display as Gold/Yellow pins; Universities must display as Deep Blue pins.

   - Visited State: Swaps the pin marker styles to an ultra-faded, desaturated Light Gray (opacity: 0.35) or drops the layer from the viewport entirely based on filtering status.

2. Marker Clustering: All coordinates must be assigned directly to an instance of L.markerClusterGroup(). Nearby pins must cluster dynamically based on zoom settings to conserve mobile rendering cycles.

3. Popup Interface: Tapping any marker pin initiates a clean popup container detailing the location Name, Class/Type, City, State, a large native "Navigate" CTA button, and a large "Mark as Visited" toggle checkbox.

### C. The Stateful Slide-Up Checklist Drawer

1. Layout & Accordions: A floating action layout containing a slide-up panel. Data must group hierarchically: US State (Accordion) -> Type (Tabs: Temples/Universities) -> Alphabetic Grid List.

2. Two-Way Synchronization: Tapping a checkbox in the list drawer must instantly alter the corresponding map marker's style in the viewport, and vice versa.

### D. Offline State Retention (Persistence)

- Every single interaction changing a location's completion state must immediately serialize to browser localStorage using the location's unique id string as the key structure.

- Hard webpage reloads or driving through cellular dead zones must not clear or degrade user tracking progress.

### E. Navigation Integration

- The application will delegate all geolocation routing to native device apps. 

- All "Navigate" action triggers must use the deep-link layout: [[http://maps.google.com/?q=](http://maps.google.com/?q=){lat},{lng}](http://maps.google.com/?q=](http://maps.google.com/?q=){lat},{lng}). This ensures instant execution of native Google Maps turn-by-turn routing on both iOS and Android

## Current Sprint Goal

Create a single-file mobile web application named `index.html`. 
Use Tailwind CSS via CDN for styling and Leaflet.js (OpenStreetMap) for a full-screen, highly responsive map.

Requirements:
1. The map must occupy 100% of the mobile viewport height and width. Prevent default double-tap zooming using proper mobile viewport meta tags.
2. Include the Leaflet.markercluster plugin CSS and JS via CDN links so we can smoothly handle thousands of interactive points across the country without performance lag.
3. Center the map view over the continental United States (zoom level ~4) by default.
4. Add a floating, semi-transparent header bar at the top that reads "US Road Trip Explorer".
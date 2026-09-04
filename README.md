# NNA Delivery Route Planner — Phuket 🏍️🗺️

## Overview
A university term project that models a small delivery-routing problem in Phuket as a **Travelling Salesman Problem (TSP)**, solved with the **Nearest Neighbor Algorithm (NNA)**. The backend geocodes a list of candidate locations near Patong Beach, and the frontend orders them into a route with NNA, then renders the actual driving route and live traffic on Google Maps.

![Screenshot 2024-11-26 135800](https://github.com/user-attachments/assets/c77a5a8a-f6ff-490c-9acc-60706b3bc4d7)

## How It Works
1. **Location generation** (Flask backend, `/generate`): reads a list of place names from `NLP.txt`, geocodes each one via the Google Maps Geocoding API, filters to locations within ~1–2 km of the city center (Patong Beach), and returns 6 random nearby locations.
2. **Route ordering** (client-side JS, `calculateNNARoute`): applies the Nearest Neighbor heuristic — starting from the first point, repeatedly jump to the closest unvisited point — to produce a delivery order.
3. **Route rendering**: the ordered stops are sent to the Google Maps Directions API to draw the actual driving route, with a live traffic layer and total distance shown in a draggable info box.

## Features
- 🗺️ Interactive Google Map centered on Phuket, with a live traffic layer
- 📍 Random sampling of nearby delivery points from a location dataset (`NLP.txt`)
- 🧮 Route ordering via the Nearest Neighbor (NNA) heuristic for TSP
- 🚗 Real driving directions and total distance via the Google Maps Directions API
- 🕐 Live clock and a draggable route-info box

## Tech Stack
- **Backend**: Python, Flask
- **Geocoding**: `googlemaps` (Python client for the Google Maps Geocoding API)
- **Distance filtering**: `geopy` (geodesic distance)
- **Frontend**: HTML/CSS/JavaScript, Google Maps JavaScript API (Maps, Directions, Traffic Layer)

## Getting Started

### Prerequisites
- Python 3.12
- A Google Maps API key with the **Geocoding API**, **Maps JavaScript API**, and **Directions API** enabled

### Installation
```bash
git clone https://github.com/INciD1/NNAtspPhuket.github.io.git
cd NNAtspPhuket.github.io/project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure your API key
```bash
cp .env.example .env
```
Then open `.env` and set `GOOGLE_MAPS_API_KEY` to your own key. The app reads it from the environment — nothing is hardcoded in the source anymore.

### Run locally
```bash
python app.py
```
Then open `http://localhost:5000`.

## ⚠️ Before Deploying
This project was built for local/classroom demo use. Before deploying it anywhere public:
- Restrict your Google Maps API key in Google Cloud Console (HTTP referrer restriction + limit it to only the APIs this project uses). The key is necessarily visible in the browser for the Maps JavaScript API — restricting it is the correct mitigation, not hiding it.
- Leave `FLASK_DEBUG` unset (or `false`) in production.

## Known Limitations
- Locations are drawn from a fixed, bundled dataset (`NLP.txt`), not live delivery data.
- `filter_apartments_and_condos()` (keyword-based place-type filtering) exists in `app.py` but isn't currently wired into any route.
- No real NLP model is used — location matching is plain keyword/substring filtering, not NLP-based entity extraction.

## Possible Improvements
- Actually apply the `filter_apartments_and_condos()` filtering (or replace it with a real NLP/entity-extraction step if that's still the goal).
- Cache geocoding results instead of re-geocoding the full location list on every `/generate` call.

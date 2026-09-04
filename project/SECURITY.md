# Security Policy

## Reporting a Vulnerability

This is a student term project, not a production service, but if you spot a security issue (e.g. a way to make the app leak the Google Maps API key, or an injection point), please open an issue on this repository describing the problem. There's no formal disclosure timeline since this isn't an actively maintained production app, but reports are welcome and appreciated.

## Known Security Notes

- The Google Maps API key is read from the `GOOGLE_MAPS_API_KEY` environment variable (see `.env.example`) — never commit a real key to this repo.
- Because this uses the Google Maps **JavaScript** API, the key is necessarily visible in the page source in the browser — that's expected for this API. The correct mitigation is **key restriction** in Google Cloud Console (HTTP referrer restriction + limiting the key to only the Maps JavaScript, Geocoding, and Directions APIs), not trying to hide the key.
- Flask debug mode is off by default (`FLASK_DEBUG` env var) — don't enable it in anything resembling a public deployment.

# backend/google_places_client.py
import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

TEXTSEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

def search_places(
    query: str,
    location_str: str,
    max_price_level: Optional[int] = None,
    limit: int = 10,
) -> List[Dict]:
    """
    Use Google Places Text Search to find restaurants near a location string.
    query: e.g. "spicy chicken"
    location_str: e.g. "San Jose, CA"
    """
    if not PLACES_API_KEY:
        raise RuntimeError("GOOGLE_PLACES_API_KEY not set")

    params = {
        "query": f"{query} restaurant {location_str}",
        "type": "restaurant",
        "key": PLACES_API_KEY,
    }

    if max_price_level is not None:
        # Google price_level is 0–4; we just pass maxprice and filter later if needed
        params["maxprice"] = max_price_level

    resp = requests.get(TEXTSEARCH_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    if limit is not None:
        results = results[:limit]
    return results


def place_to_checkout_url(place_id: str) -> str:
    """Build a Google Maps URL that opens the place."""
    return f"https://www.google.com/maps/place/?q=place_id:{place_id}"

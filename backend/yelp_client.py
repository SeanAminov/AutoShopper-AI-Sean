# backend/yelp_client.py
import os
import requests
from typing import List, Dict, Optional

YELP_API_KEY = os.environ.get("YELP_API_KEY")

BASE_URL = "https://api.yelp.com/v3"

def search_restaurants(
    term: str,
    location: str,
    max_price_level: Optional[int] = None,
    limit: int = 10,
) -> List[Dict]:
    """
    Search Yelp for restaurants matching a term near a location.
    Price levels: 1 = $, 2 = $$, 3 = $$$, 4 = $$$$
    """
    if not YELP_API_KEY:
        raise RuntimeError("YELP_API_KEY not set")

    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {
        "term": term or "food",
        "location": location,
        "categories": "restaurants",
        "limit": limit,
        "sort_by": "rating",  # prioritize high rating
    }
    if max_price_level:
        # Yelp expects comma-separated price levels: "1,2"
        params["price"] = ",".join(str(i) for i in range(1, max_price_level + 1))

    resp = requests.get(f"{BASE_URL}/businesses/search", headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get("businesses", [])

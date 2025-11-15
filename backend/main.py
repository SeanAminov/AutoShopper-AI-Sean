# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any, Dict
import time

from llm_utils import parse_prompt_with_llm, select_place_and_item
from google_places_client import search_places, place_to_checkout_url

app = FastAPI()

# CORS: open for hackathon
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrderRequest(BaseModel):
    prompt: str
    location: Optional[str] = None  # e.g. "San Jose, CA"

@app.get("/health")
def health() -> Dict[str, bool]:
    return {"ok": True}

@app.post("/api/order")
def create_order(req: OrderRequest) -> Dict[str, Any]:
    try:
        print(f"[api/order] prompt={req.prompt!r}, location={req.location!r}")

        if not req.location:
            return {"status": "error", "error": "Location is required."}

        # 1) LLM: understand the prompt
        constraints = parse_prompt_with_llm(req.prompt)
        cuisine = constraints.get("cuisine") or "food"
        max_price = constraints.get("max_price")

        # Map max_price -> Google price_level 0–4 (rough heuristic)
        max_price_level = None
        if isinstance(max_price, (int, float)):
            if max_price <= 10:
                max_price_level = 1
            elif max_price <= 20:
                max_price_level = 2
            elif max_price <= 35:
                max_price_level = 3
            else:
                max_price_level = 4

        # 2) Google Places: search for candidates
        places = search_places(
            query=cuisine,
            location_str=req.location,
            max_price_level=max_price_level,
            limit=5,
        )

        if not places:
            return {
                "status": "error",
                "error": "No restaurants found matching your request."
            }

        # 3) LLM: pick best place + item
        selection = select_place_and_item(req.prompt, places)
        idx = selection.get("place_index", 0)
        if not isinstance(idx, int) or idx < 0 or idx >= len(places):
            idx = 0

        chosen = places[idx]
        item_name = selection.get("item_name", "Recommended item")
        est_price = selection.get("estimated_total_price") or max_price or 0

        address = chosen.get("formatted_address", "Address unavailable")
        place_id = chosen.get("place_id")
        checkout_url = place_to_checkout_url(place_id) if place_id else ""

        # Response shape that matches your current frontend
        data = {
            "platform": "Google Maps",
            "restaurant_name": chosen.get("name", "Unknown restaurant"),
            "drink_name": item_name,
            "total_price": est_price,
            "eta_minutes": 25,  # still fake for now
            "restaurant_address": address,
            "checkout_url": checkout_url,
        }

        return {
            "status": "ok",
            "data": data,
            "timestamp": int(time.time()),
        }

    except Exception as e:
        print("[api/order][error]", e)
        return {"status": "error", "error": "Internal error while planning order."}

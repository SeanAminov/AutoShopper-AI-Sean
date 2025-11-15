# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any, Dict
import time

from llm_utils import parse_prompt_with_llm, select_restaurant_and_item
from yelp_client import search_restaurants

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # hackathon mode
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrderRequest(BaseModel):
    prompt: str
    location: Optional[str] = None

@app.post("/api/order")
def create_order(req: OrderRequest) -> Dict[str, Any]:
    try:
        print(f"[api/order] prompt={req.prompt!r}, location={req.location!r}")

        if not req.location:
            return {"status": "error", "error": "Location is required."}

        # 1) LLM parses constraints
        constraints = parse_prompt_with_llm(req.prompt)
        cuisine_term = constraints.get("cuisine") or "food"
        max_price = constraints.get("max_price")

        # 2) Map max_price -> Yelp price level
        max_price_level = None
        if max_price:
            if max_price <= 10:
                max_price_level = 1
            elif max_price <= 20:
                max_price_level = 2
            elif max_price <= 35:
                max_price_level = 3
            else:
                max_price_level = 4

        # 3) Get Yelp candidates
        businesses = search_restaurants(
            term=cuisine_term,
            location=req.location,
            max_price_level=max_price_level,
            limit=5,
        )
        if not businesses:
            return {
                "status": "error",
                "error": "No restaurants found matching your request."
            }

        # 4) Let the LLM choose best restaurant + item
        selection = select_restaurant_and_item(req.prompt, businesses)
        idx = selection.get("restaurant_index", 0)
        if idx < 0 or idx >= len(businesses):
            idx = 0

        best = businesses[idx]
        item_name = selection.get("item_name", "Recommended item")
        est_price = selection.get("estimated_total_price") or max_price or 0

        display_address = ", ".join(best["location"]["display_address"])
        yelp_url = best["url"]

        data = {
            "platform": "Yelp",
            "restaurant_name": best["name"],
            "drink_name": item_name,
            "total_price": est_price,
            "eta_minutes": 25,  # still fake; you can improve later
            "restaurant_address": display_address,
            "checkout_url": yelp_url,
        }

        return {
            "status": "ok",
            "data": data,
            "timestamp": int(time.time()),
        }

    except Exception as e:
        print("[api/order][error]", e)
        return {"status": "error", "error": "Internal error while planning order."}

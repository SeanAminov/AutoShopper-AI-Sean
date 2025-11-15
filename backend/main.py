# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI()

class PlanOrderRequest(BaseModel):
    prompt: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/plan-order")
def plan_order(req: PlanOrderRequest) -> Dict[str, Any]:
    # TODO: LLM + menu search here
    fake_plan = {
        "restaurant": {
            "id": "firewok",
            "name": "FireWok",
            "rating": 4.7,
            "distance_km": 1.2,
        },
        "item": {
            "id": "spicy_chicken_bowl",
            "name": "Spicy Chicken Bowl",
            "price": 12.99,
        },
        "explanation": "Picked FireWok because it's close, highly rated, and spicy chicken.",
    }
    return fake_plan

class ConfirmOrderRequest(BaseModel):
    restaurantId: str
    itemId: str
    address: str

@app.post("/confirm-order")
def confirm_order(req: ConfirmOrderRequest):
    order_id = f"ord_{int(__import__('time').time())}"
    return {"orderId": order_id, "status": "placed"}

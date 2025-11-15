# backend/llm_utils.py
import os
import json
from typing import Dict, List, Any

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ---------- 1) Parse prompt -> constraints ----------

def parse_prompt_with_llm(prompt: str) -> Dict[str, Any]:
    """
    Use an LLM to extract structured constraints from the user's prompt.
    """
    system_msg = (
        "You are an assistant that extracts food-ordering constraints "
        "from a free-text user prompt. "
        "Respond ONLY with a JSON object with keys: "
        "cuisine (string or null), "
        "max_price (number or null), "
        "max_distance_km (number or null), "
        "spice_level (string or null), "
        "dietary (array of strings)."
    )

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",  # or whatever model you have access to
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
        ],
    )

    content = resp.choices[0].message.content
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Fallback minimal structure if the LLM glitches
        data = {
            "cuisine": None,
            "max_price": None,
            "max_distance_km": 5,
            "spice_level": None,
            "dietary": [],
        }
    return data

def select_restaurant_and_item(prompt: str, businesses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Given the user's prompt and a list of Yelp businesses (dicts),
    ask the LLM to pick the best restaurant and suggest an item.

    Returns JSON like:
      {
        "restaurant_index": 0,
        "item_name": "Spicy Chicken Rice Bowl",
        "estimated_total_price": 13.50
      }
    """
    # Make a compact version of businesses to avoid huge prompts
    condensed = []
    for i, b in enumerate(businesses):
        condensed.append({
            "index": i,
            "name": b.get("name"),
            "rating": b.get("rating"),
            "price": b.get("price"),
            "categories": [c.get("title") for c in b.get("categories", [])],
            "address": ", ".join(b.get("location", {}).get("display_address", [])),
            "url": b.get("url"),
        })

    system_msg = (
        "You are an AI food ordering assistant. "
        "The user describes what they want to eat. "
        "You are given a list of candidate restaurants with ratings and categories. "
        "Choose the single best restaurant and suggest a specific dish or drink "
        "that matches the user's request. "
        "Respond ONLY with a JSON object with keys: "
        "restaurant_index (integer), "
        "item_name (string), "
        "estimated_total_price (number)."
    )

    user_msg = (
        "User prompt:\n"
        f"{prompt}\n\n"
        "Candidate restaurants (JSON list):\n"
        f"{json.dumps(condensed, ensure_ascii=False)}"
    )

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
    )
    content = resp.choices[0].message.content
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: just pick the first business
        data = {
            "restaurant_index": 0,
            "item_name": "Recommended item",
            "estimated_total_price": 0.0,
        }
    return data

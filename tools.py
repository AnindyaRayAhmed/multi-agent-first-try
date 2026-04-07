"""Simulated MCP-style tools (DB + memory + brand store)."""

from typing import Any, Dict, List
from .db import fetch_campaigns, init_db, insert_campaign, save_brand, get_brand, init_brand_table

# Ensure DB is initialized as soon as tools module is loaded.
init_db()
init_brand_table()

def save_campaign(product: str, idea: Dict[str, Any], copy: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
    """Saves a generated campaign with its idea, copy, and plan to the database."""
    try:
        campaign_id = insert_campaign(
            product=product,
            idea=idea,
            copy=copy,
            plan=plan,
        )
        return {"campaign_id": campaign_id}
    except Exception as e:
        return {"error": str(e)}

def get_campaigns() -> List[Dict[str, Any]]:
    """Return previously saved campaigns."""
    return fetch_campaigns()

def save_brand_tool(brand: str, tone: str, colors: str) -> Dict[str, str]:
    """Saves brand guidelines including brand name, tone, and colors to the database."""
    return save_brand(brand, tone, colors)

def get_brand_tool(brand: str) -> Dict[str, str]:
    """Retrieves saved brand guidelines (tone and colors) for a given brand name."""
    return get_brand(brand)

def get_campaigns_tool(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieves the list of previously saved marketing campaigns."""
    return fetch_campaigns()

def schedule_campaign_tool(product: str, schedule: str) -> Dict[str, str]:
    """Schedules the campaign posting plan for a given product."""
    return {
        "status": "scheduled",
        "product": product,
        "schedule": schedule
    }

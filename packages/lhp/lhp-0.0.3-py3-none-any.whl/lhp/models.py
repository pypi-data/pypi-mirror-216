"""Asynchronous client for the Länderübergreifendes Hochwasserportal API."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CurrentWaterLevel(BaseModel):
    """Current weather data."""

    water_level: float = Field(..., alias="W_float")
    flood: int = Field(..., alias="HW")
    flood_text: str = Field(..., alias="HW_TXT")

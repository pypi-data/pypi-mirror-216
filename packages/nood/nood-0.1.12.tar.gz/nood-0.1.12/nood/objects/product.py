from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Variant(BaseModel):
    id: Optional[str]
    value: str
    stock: Optional[int]
    atc_url: Optional[str]
    direct_url: Optional[str]

    class Config:
        allow_population_by_field_name = True


class Product(BaseModel):
    monitor_id: Optional[int]
    url: str
    name: str
    brand: Optional[str]
    price: Optional[float]
    currency: Optional[str]
    sku: Optional[str]
    variants: Optional[List[Variant]] = []
    thumbnail_url: Optional[str]
    region: Optional[str]
    additional_information: Optional[str]
    found_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True

from typing import Any
from pydantic import Field
from fastkit_core.validation import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema
)


class ProductCreate(BaseCreateSchema):
    sku: str = Field(min_length=1, max_length=100, description="Product SKU (unique)")
    name: str = Field(description="Translated product names")
    description: str = Field(default_factory=dict, description="Translated descriptions")
    price: float = Field(gt=0, description="Price (must be positive)")
    stock: int = Field(default=0, ge=0, description="Stock quantity")


class ProductUpdate(BaseUpdateSchema):
    """Schema for updating a product."""
    sku: str | None = Field(None, min_length=1, max_length=100)
    name: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    is_active: bool | None = None


class ProductResponse(BaseSchema):
    """Schema for product in responses."""
    id: int
    sku: str
    slug: str
    name: str
    description: str
    price: float
    stock: int
    is_active: bool

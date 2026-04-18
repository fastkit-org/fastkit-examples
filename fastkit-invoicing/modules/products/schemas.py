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
    """
    Schema for Product API responses.

    Include all fields that should be returned to the client.
    Always include id and timestamps from BaseWithTimestamps.

    model_config from_attributes=True is required for SQLAlchemy model mapping.
    """
    id: int
    # Add your fields here
    # Example:
    # name: str
    # price: float
    # description: str | None = None
    created_at: Any = None
    updated_at: Any = None

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
    """
    Schema for updating an existing Product.

    All fields should be optional (| None = None) to support partial updates.

    Example:
        name: str | None = None
        price: float | None = None
    """
    pass  # Replace with actual fields


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

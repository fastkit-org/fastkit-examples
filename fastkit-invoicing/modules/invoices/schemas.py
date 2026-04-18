from typing import Any
from pydantic import Field
from fastkit_core.validation import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    # min_length,       # Uncomment for string min length: name: str = min_length(3)
    # max_length,       # Uncomment for string max length: name: str = max_length(100)
    # length,           # Uncomment for string length range: name: str = length(3, 100)
    # min_value,        # Uncomment for numeric min: price: float = min_value(0.01)
    # max_value,        # Uncomment for numeric max: stock: int = max_value(1000)
    # between,          # Uncomment for numeric range: rating: float = between(1.0, 5.0)
    # pattern,          # Uncomment for regex: code: str = pattern(r'^[A-Z]{3}$')
    # SlugValidatorMixin,       # Uncomment if model uses SlugMixin
    # PasswordValidatorMixin,   # Uncomment for standard password validation
    # StrongPasswordValidatorMixin,  # Uncomment for strong password validation
    # UsernameValidatorMixin,   # Uncomment for username validation
)


class InvoiceCreate(BaseCreateSchema):
    client_id: int = Field(gt=0, description="Client ID")
    invoice_number: str


class InvoiceUpdate(BaseUpdateSchema):
    """
    Schema for updating an existing Invoice.

    All fields should be optional (| None = None) to support partial updates.

    Example:
        name: str | None = None
        price: float | None = None
    """
    pass  # Replace with actual fields


class InvoiceResponse(BaseSchema):
    """
    Schema for Invoice API responses.

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

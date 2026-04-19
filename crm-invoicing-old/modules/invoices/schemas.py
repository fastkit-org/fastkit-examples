from typing import Optional

from fastkit_core.validation import BaseSchema
from app.models.enums import InvoicesStatus
from app.schemas.invoice_item import InvoiceItemCreate, InvoiceItemResponse
from modules.clients.schemas import ClientResponse
from pydantic import Field, computed_field, field_serializer
from datetime import datetime
from fastkit_core.i18n import _


class InvoiceCreate(BaseSchema):
    client_id: int = Field(gt=0, description="Client ID")
    items: list[InvoiceItemCreate] = Field(min_length=1, description="Invoice items (min: 1)")
    invoice_number: str

class InvoiceUpdate(BaseSchema):
    status: InvoicesStatus | None = None


class InvoiceResponse(BaseSchema):
    """Schema for invoice in responses."""
    id: int
    invoice_number: str
    client_id: int
    status: InvoicesStatus
    pdf_path: str | None
    created_at: datetime | None = None

    # Nested relationships (optional)
    items: list[InvoiceItemResponse] = []
    client: Optional[ClientResponse] = None

    model_config = {"from_attributes": True}

    @field_serializer('created_at')
    def serialize_datetime(self, dt: datetime | None, _info):
        if dt is None:
            return None
        return dt.strftime("%m/%d/%Y")

    @computed_field
    @property
    def total_amount(self) -> float:
        return sum(item.quantity * item.unit_price for item in self.items)

    @computed_field
    @property
    def status_label(self) -> str:
        return _(f"invoices.statuses.{self.status.lower()}")
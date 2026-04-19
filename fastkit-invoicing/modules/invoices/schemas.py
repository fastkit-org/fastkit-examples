from typing import Any, Optional
from pydantic import Field, computed_field, field_serializer
from datetime import datetime
from fastkit_core.i18n import _
from app.models.enums import InvoicesStatus
from fastkit_core.validation import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema
)

from modules.clients.schemas import ClientResponse
from modules.invoice_items.schemas import InvoiceItemCreate, InvoiceItemResponse


class InvoiceCreate(BaseCreateSchema):
    client_id: int = Field(gt=0, description="Client ID")
    items: list[InvoiceItemCreate] = Field(min_length=1, description="Invoice items (min: 1)")
    invoice_number: str


class InvoiceUpdate(BaseUpdateSchema):
    status: InvoicesStatus | None = None


class InvoiceResponse(BaseSchema):
    id: int
    invoice_number: str
    client_id: int
    status: InvoicesStatus
    pdf_path: str | None
    created_at: datetime | None = None

    # Nested relationships (optional)
    client: Optional[ClientResponse] = None
    items: list[InvoiceItemResponse] = []

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

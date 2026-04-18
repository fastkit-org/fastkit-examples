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


class InvoiceCreate(BaseCreateSchema):
    client_id: int = Field(gt=0, description="Client ID")
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


    @field_serializer('created_at')
    def serialize_datetime(self, dt: datetime | None, _info):
        if dt is None:
            return None
        return dt.strftime("%m/%d/%Y")

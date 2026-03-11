from typing import Optional
from fastkit_core.database import BaseWithTimestamps, SoftDeleteMixin, IntIdMixin
from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.enums import InvoicesStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.clients.models import Client
    from app.models.invoice_item import InvoiceItem

class Invoice(IntIdMixin, BaseWithTimestamps, SoftDeleteMixin):
    __tablename__ = "invoices"

    invoice_number: Mapped[str] = mapped_column(String(20), unique=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    pdf_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[InvoicesStatus] = mapped_column(
        Enum(InvoicesStatus, name="status"),
        default=InvoicesStatus.PENDING,
        nullable=False
    )

    client: Mapped["Client"] = relationship(back_populates="invoices")
    items: Mapped[list["InvoiceItem"]] = relationship(
        back_populates="invoice",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
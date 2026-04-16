from sqlalchemy import JSON, String, Numeric
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastkit_core.database import BaseWithTimestamps, SoftDeleteMixin, TranslatableMixin, IntIdMixin, SlugMixin

if TYPE_CHECKING:
    from app.models.invoice_item import InvoiceItem

class Product(IntIdMixin, BaseWithTimestamps, SoftDeleteMixin, TranslatableMixin, SlugMixin):
    __tablename__ = "products"
    __translatable__ = ['name', 'description']

    sku: Mapped[str] = mapped_column(String(100), unique=True)
    name:  Mapped[dict] = mapped_column(JSON)
    description:  Mapped[dict] = mapped_column(JSON)
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

    invoice_items: Mapped[list["InvoiceItem"]] = relationship(back_populates="product")

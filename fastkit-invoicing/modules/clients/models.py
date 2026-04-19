from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List
from fastkit_core.database import (
    BaseWithTimestamps,
    IntIdMixin,
    SoftDeleteMixin,
)
from app.models.enums import Languages

if TYPE_CHECKING:
    from modules.invoices.models import Invoice


class Clients(BaseWithTimestamps, IntIdMixin, SoftDeleteMixin):
    __tablename__ = "clients"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255))
    language: Mapped[Languages] = mapped_column(
        Enum(Languages, name="language"),
        default=Languages.EN,
        nullable=False
    )

    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)

    invoices: Mapped[List["Invoice"]] = relationship(back_populates="client")
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from fastkit_core.database import (
    BaseWithTimestamps,
    IntIdMixin,
    # UUIDMixin,          # Uncomment to use UUID as primary key instead of IntIdMixin
    SoftDeleteMixin,    # Uncomment to enable soft delete (deleted_at)
    # SlugMixin,          # Uncomment to add slug field (slug)
    # PublishableMixin,   # Uncomment to add published_at field
    # TranslatableMixin,  # Uncomment for multi-language field support
)
from app.models.enums import Languages

class Clients(BaseWithTimestamps, IntIdMixin, SoftDeleteMixin):
    __tablename__ = "clientses"

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
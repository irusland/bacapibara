import sqlalchemy as sa
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

from api.storage.database.base import Base


class Messages(Base):
    chat_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)

    __table_args__ = (
        Index(
            "ix_tsvector_text",
            sa.text("to_tsvector('russian'::regconfig, text::text)"),
            postgresql_using="gin",
        ),
    )

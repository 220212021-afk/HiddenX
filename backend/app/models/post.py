from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, func, true
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        CheckConstraint("char_length(content) <= 280", name="content_max_280"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    content: Mapped[str] = mapped_column(String(280))
    image_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

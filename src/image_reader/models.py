from sqlalchemy import String, TIMESTAMP, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Images(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    image_name: Mapped[str] = mapped_column(
        String(length=100), nullable=False
    )
    image_size: Mapped[str] = mapped_column(
        String, nullable=False
    )
    last_edit_at: Mapped[str] = mapped_column(
        String
    )

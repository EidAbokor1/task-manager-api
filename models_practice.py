from sqlalchemy import Identity, Text, false
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    completed: Mapped[bool] = mapped_column(server_default=false())
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, BigInteger
from ..db import db


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(Text)
    moons_count: Mapped[int]

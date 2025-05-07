from ..db import db
from sqlalchemy import BIGINT, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .planet import Planet


class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    size_km: Mapped[int] = mapped_column(BIGINT)
    description: Mapped[str] = mapped_column(Text)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="moons")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "size_km": self.size_km,
            "description": self.description,
            "planet": self.planet.name if self.planet_id else None
        }

    @classmethod
    def from_dict(cls, moon_data):
        new_moon = cls(
            name=moon_data["name"],
            description=moon_data["description"],
            size_km=moon_data["size_km"],
            planet_id=moon_data["planet_id"])

        return new_moon

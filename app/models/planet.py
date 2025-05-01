from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from ..db import db


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(Text)
    moons_count: Mapped[int]

    def to_dict(self):
        planet_dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "moons_count": self.moons_count
        }

        return planet_dict

    @classmethod
    def from_dict(cls, planet_data):
        new_planet = cls(
            name=planet_data["name"],
            description=planet_data["description"],
            moons_count=planet_data["moons_count"])

        return new_planet

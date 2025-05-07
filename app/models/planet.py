from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
from sqlalchemy import Text



class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(Text)
    moons_count: Mapped[int]
    moon_id: Mapped[Optional[int]] = mapped_column(ForeignKey("moon.id"))
    planets: Mapped[list["Planet"]] = relationship(back_populates="moon")
    moon: Mapped[Optional["Moon"]] = relationship(back_populates="planets")

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

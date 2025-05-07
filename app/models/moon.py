from ..db import db
from sqlalchemy import BIGINT, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    size_km: Mapped[BIGINT]
    description: Mapped[str] = mapped_column(Text)
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "size_km": self.size_km,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, moon_data):
        new_moon = cls(name=moon_data["name"], description=moon_data["description"], size_km=moon_data["size_km"])
        return new_moon
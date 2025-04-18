from flask import Blueprint
from ..models.planet import planets

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


@planets_bp.get("")
def get_all_planets():
    planets_response = []
    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name, 
                "description": planet.description,
                "moons_count": planet.moons_count
            }
        )
    return planets_response

@planets_bp.get("/<id>")

def get_planets_by_id(id):
    id = int(id)

    for planet in planets:
        if planet.id == id:
            planet_dict = dict(
                id = planet.id,
                name = planet.name,
                description = planet.description,
                moons_count = planet.moons_count
            )
            return planet_dict

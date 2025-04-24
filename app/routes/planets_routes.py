from flask import Blueprint, abort, make_response
# from ..models.planet import planets

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
    planet = validate_planet(id)

    planet_dict = dict(
        id = planet.id,
        name = planet.name,
        description = planet.description,
        moons_count = planet.moons_count
    )

    return planet_dict


def validate_planet(id):
    try:
        id = int(id)
    except ValueError:
        response = {"message": f"Planet id {id} is invalid"}
        abort(make_response(response, 400))

    for planet in planets:
        if planet.id == id:
            return planet

    response = {"message": f"Planet with id:{id} not found"}
    abort(make_response(response, 404))

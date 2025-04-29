from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.planet import Planet


planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    moons_count = request_body["moons_count"]

    new_planet = Planet(name=name, description=description, moons_count=moons_count)
    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "moons_count": new_planet.moons_count
    }
    return response, 201


@planets_bp.get("")
def get_all_planets():
    query = db.select(Planet)

    description_param = request.args.get("description")
    if description_param:
        query = db.where(Planet.name == description_param)
        
    
    query = db.order_by(Planet.name.desc)

    planets = db.session.scalars(query)
    planets_response = []

    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "moons_count": planet.moons_count,
            }
        )
    return planets_response



@planets_bp.get("/<id>")
def get_one_planet(id):
    planet = validate_planet(id)
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "moons_count": planet.moons_count
    }


@planets_bp.put("/<id>")
def update_planet(id):
    planet = validate_planet(id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.moons_count = request_body["moons_count"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@planets_bp.delete("/<id>")
def delete_planet(id):
    planet = validate_planet(id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


def validate_planet(id):
    try:
        id = int(id)
    except ValueError:
        response = {"message": f"Planet id {id} is invalid"}
        abort(make_response(response, 400))

    query = db.select(Planet).where(Planet.id == id)
    planet = db.session.scalar(query)

    if not planet:
        response = {"message": f"Planet with id:{id} not found"}
        abort(make_response(response, 404))

    return planet

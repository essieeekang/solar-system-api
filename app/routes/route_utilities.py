from flask import abort, make_response
from ..db import db


def validate_planet(cls, id):
    try:
        id = int(id)
    except ValueError:
        response = {"message": f"{cls.__name__} id {id} is invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} with id:{id} not found"}
        abort(make_response(response, 404))

    return model

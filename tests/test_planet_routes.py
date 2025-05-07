from app.db import db
from app.models.planet import Planet
from app.models.moon import Moon
from app.routes.route_utilities import validate_model
from werkzeug.exceptions import HTTPException
import pytest


def test_get_all_planets_returns_empty_list_when_db_is_empty(client):
    # act
    response = client.get("/planets")

    # assert
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_all_planets_returns_all_planets(client, one_planet):
    # act
    response = client.get("/planets")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["id"] == one_planet.id
    assert response_body[0]["name"] == one_planet.name
    assert response_body[0]["description"] == one_planet.description
    assert response_body[0]["moons_count"] == one_planet.moons_count


def test_get_all_planets_moons_count_param(client, two_planets):
    # act
    response = client.get("/planets?moons_count=0")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["id"] == 2
    assert response_body[0]["name"] == "Venus"
    assert response_body[0]["description"] == "Earth's closest neighbor, a hot and dense planet with a thick, toxic atmosphere."
    assert response_body[0]["moons_count"] == 0


def test_get_all_planets_description_param(client, two_planets):
    # act
    response = client.get("/planets?description=ice")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["id"] == 1
    assert response_body[0]["name"] == "Mars"
    assert response_body[0]["description"] == "The Red Planet, with a thin atmosphere, polar ice caps, and evidence of past water"
    assert response_body[0]["moons_count"] == 2


def test_get_all_planets_description_moons_count_params(client, two_planets):
    # act
    response = client.get("/planets?description=planet&moons_count=0")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["id"] == 2
    assert response_body[0]["name"] == "Venus"
    assert response_body[0]["description"] == "Earth's closest neighbor, a hot and dense planet with a thick, toxic atmosphere."
    assert response_body[0]["moons_count"] == 0


def test_get_one_planet_returns_seeded_planet(client, one_planet):
    # act
    response = client.get(f"/planets/{one_planet.id}")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert response_body["id"] == one_planet.id
    assert response_body["name"] == one_planet.name
    assert response_body["description"] == one_planet.description
    assert response_body["moons_count"] == one_planet.moons_count


def test_get_one_planet_returns_404(client):
    # act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet with id:1 not found"}


def test_create_planet_happy_path(client):
    # arrange
    EXPECTED_PLANET = {
        "name": "Venus",
        "description": "Earth's closest neighbor, a hot and dense planet with a thick, toxic atmosphere",
        "moons_count": 0
    }

    # act
    response = client.post("/planets", json=EXPECTED_PLANET)
    response_body = response.get_json()

    # assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["name"] == EXPECTED_PLANET["name"]
    assert response_body["description"] == EXPECTED_PLANET["description"]
    assert response_body["moons_count"] == EXPECTED_PLANET["moons_count"]

    # We could further check that the DB was actually updated
    query = db.select(Planet).where(Planet.id == 1)
    new_planet = db.session.scalar(query)  # compare these values to EXPECTED

    assert new_planet.id == 1
    assert new_planet.name == EXPECTED_PLANET["name"]
    assert new_planet.description == EXPECTED_PLANET["description"]
    assert new_planet.moons_count == EXPECTED_PLANET["moons_count"]


def test_create_planet_missing_attribute(client):
    # arrange
    incomplete_data = {"name": "Mercury"}

    # act
    response = client.post("/planets", json=incomplete_data)
    response_body = response.get_json()

    # assert
    assert response.status_code == 400
    assert response_body == {"message": "Invalid request: missing data"}


def test_create_planet_with_additional_attributes(client):
    # arrange
    planet_data = {
        "name": "Venus",
        "description": "Earth's closest neighbor, a hot and dense planet with a thick, toxic atmosphere",
        "moons_count": 0,
        "position_from_sun": 2
    }

    # act
    response = client.post("/planets", json=planet_data)
    response_body = response.get_json()

    # assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["name"] == planet_data["name"]
    assert response_body["description"] == planet_data["description"]
    assert response_body["moons_count"] == planet_data["moons_count"]


def test_from_dict_returns_planet():
    # arrange
    planet = {
        "name": "Venus",
        "description": "Earth's closest neighbor, a hot and dense planet with a thick, toxic atmosphere",
        "moons_count": 0
    }

    # act
    new_planet = Planet.from_dict(planet)

    # act and assert
    assert new_planet.name == "Venus"
    assert new_planet.description == "Earth's closest neighbor, a hot and dense planet with a thick, toxic atmosphere"
    assert new_planet.moons_count == 0


def test_from_dict_with_missing_data():
    # arrange
    incomplete_data = {"name": "Mercury"}

    # act and assert
    with pytest.raises(KeyError):
        Planet.from_dict(incomplete_data)


def test_to_dict_no_missing_data():
    # arrange
    test_data = Planet(
        id=1,
        name="Venus",
        description="Earth's closest neighbor, a hot and dense planet with a thick, toxic atmosphere",
        moons_count=0
        )

    # act
    result = test_data.to_dict()

    # assert
    assert result["id"] == 1
    assert result["name"] == "Venus"
    assert result["description"] == "Earth's closest neighbor, a hot and dense planet with a thick, toxic atmosphere"
    assert result["moons_count"] == 0
    assert "moons" in result


def test_to_dict_missing_data():
    # arrange
    test_data = Planet(id=1, moons_count=0)

    # act
    result = test_data.to_dict()

    # assert
    assert result["id"] == 1
    assert result["moons_count"] == 0
    assert result["description"] is None
    assert result["name"] is None
    assert "moons" in result


def test_update_planet(client, one_planet):
    # arrange
    test_data = {
        "name": "Mercury",
        "description": "The smallest and closest planet to the Sun, known for its fast orbit and cratered surface.",
        "moons_count": 0
    }

    # act
    response = client.put("/planets/1", json=test_data)

    # assert
    assert response.status_code == 204

    # checking if actual database was updated
    query = db.select(Planet).where(Planet.id == 1)
    updated_planet = db.session.scalar(query)

    assert updated_planet.id == 1
    assert updated_planet.name == test_data["name"]
    assert updated_planet.description == test_data["description"]
    assert updated_planet.moons_count == test_data["moons_count"]


def test_update_nonexisting_planet(client):
    # arrange
    test_data = {
        "name": "Mercury",
        "description": "The smallest and closest planet to the Sun, known for its fast orbit and cratered surface.",
        "moons_count": 0
    }

    # act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet with id:1 not found"}


def test_delete_planet(client, one_planet):
    # act
    response = client.delete("/planets/1")

    # assert
    assert response.status_code == 204

    # checking if actual database was updated
    planets = db.session.query(Planet).all()

    assert len(planets) == 0


def test_validate_model(one_planet):
    # act
    result_planet = validate_model(Planet, 1)

    # assert
    assert result_planet.id == 1
    assert result_planet.name == "Mars"
    assert result_planet.description == "The Red Planet, with a thin atmosphere, polar ice caps, and evidence of past water"
    assert result_planet.moons_count == 2


def test_validate_model_nonexistent_planet(one_planet):
    # act and assert
    with pytest.raises(HTTPException):
        validate_model(Planet, 3)


def test_validate_model_invalid_id(client):
    # act and assert
    with pytest.raises(HTTPException):
        validate_model(Planet, "tatooine")



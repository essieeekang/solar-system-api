from app.db import db
from app.models.moon import Moon
from app.models.planet import Planet


def test_get_all_moons_of_planet_with_no_moons(client, one_planet):
    # act
    response = client.get(f"/planets/{one_planet.id}/moons")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_moons_of_planet_with_moons(client, one_planet, two_moons):
    # act
    response = client.get(f"/planets/{one_planet.id}/moons")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert len(response_body) == 2
    

    assert response_body[0]["name"] == "Phobos"
    assert response_body[1]["name"] == "Deimos"


def test_create_moon_with_planet_happy_path(client, one_planet):
    # arrange
    EXPECTED_MOON = {
        "name": "Phobos",
        "description": "Larger of Mars' two moons, heavily cratered and irregularly shaped.",
        "size_km": 22
    }

    # act
    response = client.post(f"/planets/{one_planet.id}/moons", json=EXPECTED_MOON)
    response_body = response.get_json()

    # assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["name"] == EXPECTED_MOON["name"]
    assert response_body["description"] == EXPECTED_MOON["description"]
    assert response_body["size_km"] == EXPECTED_MOON["size_km"]
    assert response_body["planet"] == one_planet.name

  
    query = db.select(Moon).where(Moon.id == 1)
    new_moon = db.session.scalar(query)

    assert new_moon.id == 1
    assert new_moon.name == EXPECTED_MOON["name"]
    assert new_moon.description == EXPECTED_MOON["description"]
    assert new_moon.size_km == EXPECTED_MOON["size_km"]
    assert new_moon.planet_id == one_planet.id


def test_create_moon_with_invalid_planet_id(client):
    # arrange
    MOON_DATA = {
        "name": "Phobos",
        "description": "Larger of Mars' two moons, heavily cratered and irregularly shaped.",
        "size_km": 22
    }

    # act
    response = client.post("/planets/999/moons", json=MOON_DATA)
    response_body = response.get_json()

    # assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet with id:999 not found"}


def test_create_moon_missing_attribute(client, one_planet):
    # arrange
    incomplete_data = {"name": "Phobos"}

    # act
    response = client.post(f"/planets/{one_planet.id}/moons", json=incomplete_data)
    response_body = response.get_json()

    # assert
    assert response.status_code == 400
    assert "Invalid request: missing" in response_body["message"]


def test_moon_to_dict_method(client, one_planet):
    # arrange
    moon = Moon(
        id=1,
        name="Phobos",
        description="Larger of Mars' two moons, heavily cratered and irregularly shaped.",
        size_km=22,
        planet_id=one_planet.id
    )
    
    # Add to the DB so relationship is properly set up
    db.session.add(moon)
    db.session.commit()
    
    # Query back to get the correct relationship
    moon = db.session.get(Moon, 1)

    # act
    result = moon.to_dict()

    # assert
    assert result["id"] == 1
    assert result["name"] == "Phobos"
    assert result["description"] == "Larger of Mars' two moons, heavily cratered and irregularly shaped."
    assert result["size_km"] == 22
    assert result["planet"] == one_planet.name


def test_moon_from_dict_method():
    # arrange
    moon_data = {
        "name": "Phobos",
        "description": "Larger of Mars' two moons, heavily cratered and irregularly shaped.",
        "size_km": 22,
        "planet_id": 1
    }

    # act
    new_moon = Moon.from_dict(moon_data)

    # assert
    assert new_moon.name == "Phobos"
    assert new_moon.description == "Larger of Mars' two moons, heavily cratered and irregularly shaped."
    assert new_moon.size_km == 22
    assert new_moon.planet_id == 1


def test_moon_from_dict_with_missing_data():
    # arrange
    incomplete_data = {"name": "Phobos"}

    # act and assert
    import pytest
    with pytest.raises(KeyError):
        Moon.from_dict(incomplete_data)


def test_planet_to_dict_includes_moons(client, one_planet, two_moons):
    # act
    # Need to query for the planet to get the updated moons relationship
    query = db.select(Planet).where(Planet.id == one_planet.id)
    planet = db.session.scalar(query)
    result = planet.to_dict()

    # assert
    assert "moons" in result
    assert len(result["moons"]) == 2
    assert "Phobos" in result["moons"]
    assert "Deimos" in result["moons"]


    
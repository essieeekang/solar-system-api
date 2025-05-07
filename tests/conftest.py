import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.planet import Planet
from app.models.moon import Moon

load_dotenv()


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def one_planet(app):
    planet = Planet(
        name="Mars",
        description="The Red Planet, with a thin atmosphere, polar ice caps, and evidence of past water",
        moons_count=2
    )
    db.session.add(planet)
    db.session.commit()
    return planet


@pytest.fixture
def two_planets(app, one_planet):
    venus = Planet(
        name="Venus",
        description="Earth's closest neighbor, a hot and dense planet with a thick, toxic atmosphere.",
        moons_count=0
    )
    db.session.add(venus)
    db.session.commit()


@pytest.fixture
def one_moon(app, one_planet):
    moon = Moon(
        name="Phobos",
        description="Larger of Mars' two moons, heavily cratered and irregularly shaped.",
        size_km=22,
        planet_id=one_planet.id
    )
    db.session.add(moon)
    db.session.commit()
    return moon


@pytest.fixture
def two_moons(app, one_planet, one_moon):
    deimos = Moon(
        name="Deimos",
        description="Smaller of Mars' two moons, with a smooth surface.",
        size_km=12,
        planet_id=one_planet.id
    )
    db.session.add(deimos)
    db.session.commit()
    return deimos

from app import create_app
from app.db import db
from app.models.planet import Planet
from dotenv import load_dotenv

load_dotenv()

my_app = create_app()
with my_app.app_context():
    db.session.add(Planet(name="Mercury", description="The smallest and closest planet to the Sun, known for its fast orbit and cratered surface.", moons_count=0))
    db.session.add(Planet(name="Venus", description="Earth's closest neighbor, a hot and dense planet with a thick, toxic atmosphere.", moons_count=0))
    db.session.add(Planet(name="Earth", description="The only planet known to harbor life, a diverse and dynamic world with oceans, continents, and a complex ecosystem.", moons_count=1))
    db.session.add(Planet(name="Mars", description="The Red Planet, with a thin atmosphere, polar ice caps, and evidence of past water.", moons_count=2))
    db.session.add(Planet(name="Jupiter", description="The largest planet in the solar system, a gas giant with swirling clouds, a Great Red Spot, and numerous moons.", moons_count=79))
    db.session.add(Planet(name="Saturn", description="Known for its spectacular rings, Saturn is a gas giant with a yellowish color.", moons_count=82))
    db.session.add(Planet(name="Uranus", description="An ice giant with a unique axial tilt, making it appear to rotate on its side.", moons_count=27))
    db.session.add(Planet(name="Neptune", description="The farthest planet from the Sun, an ice giant with strong winds and a deep blue color.", moons_count=14))
    db.session.commit()

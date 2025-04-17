class Planet:
    def __init__(self, id, name, description, moons_count):
        self.id = id
        self.name = name
        self.description = description
        self.moons_count = moons_count

planets = [
        Planet(1, "Mercury", "The smallest planet in our solar system.", 0),
        Planet(2, "Venus", "The second planet from the Sun.", 0),
        Planet(3, "Earth", "The third planet from the Sun and the only known planet to support life.", 1),
        Planet(4, "Mars", "The fourth planet from the Sun, known as the Red Planet.", 2),

    ]

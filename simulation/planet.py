import math

class Planet:
    """
    Represents a celestial body located at the origin (0, 0).
    """

    def __init__(self, name: str, mass: float, radius: float):
        """
        Initialize the planet with its name, mass, and radius.

        Parameters:
            name (str): The name of the planet.
            mass (float): The mass of the planet in kilograms.
            radius (float): The radius of the planet in meters.
        """
        self.name = name
        self.mass = mass
        self.radius = radius

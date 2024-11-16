class Rocket:
    """
    Represents a rocket in a 2D space with position, velocity, and mass.
    
    The class provides methods to update the rocket's state and calculate 
    its properties, such as kinetic energy.
    """
    
    def __init__(self, mass: float, x: float, y: float, velocity_x: float, velocity_y: float):
        """
        Initialize the Rocket with its mass, position, and velocity.

        Parameters:
            mass (float): The mass of the rocket in kilograms.
            x (float): Initial x-coordinate in meters.
            y (float): Initial y-coordinate in meters.
            velocity_x (float): Initial velocity in the x-direction in m/s.
            velocity_y (float): Initial velocity in the y-direction in m/s.
        """
        self.mass = mass
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def kinetic_energy(self) -> float:
        """
        Calculate the rocket's kinetic energy.

        Returns:
            float: The kinetic energy of the rocket in joules.
        """
        return 0.5 * self.mass * (self.velocity_x**2 + self.velocity_y**2)

    def update_position(self, delta_x: float, delta_y: float) -> None:
        """
        Update the rocket's position based on the given changes.

        Parameters:
            delta_x (float): The change in the x-coordinate (meters).
            delta_y (float): The change in the y-coordinate (meters).
        """
        self.x += delta_x
        self.y += delta_y

    def update_velocity(self, delta_vx: float, delta_vy: float) -> None:
        """
        Update the rocket's velocity based on the given changes.

        Parameters:
            delta_vx (float): The change in the velocity in the x-direction (m/s).
            delta_vy (float): The change in the velocity in the y-direction (m/s).
        """
        self.velocity_x += delta_vx
        self.velocity_y += delta_vy

    def __repr__(self) -> str:
        """
        Return a string representation of the rocket's current state.

        Returns:
            str: A string summarizing the rocket's mass, position, and velocity.
        """
        return (f"Rocket(mass={self.mass}, x={self.x:.2f}, y={self.y:.2f}, "
                f"velocity_x={self.velocity_x:.2f}, velocity_y={self.velocity_y:.2f})")
        

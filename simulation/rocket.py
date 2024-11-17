import math

class Rocket:
    """
    Represents a rocket in a 2D space with position, velocity, and mass.
    
    The class provides methods to update the rocket's state and calculate 
    its properties, such as kinetic energy.
    """
    
    def __init__(self, mass: float, x: float, y: float, velocity_x: float, velocity_y: float, time: float):
        """
        Initialize the Rocket with its mass, position, and velocity.

        Parameters:
            mass (float): The mass of the rocket in kilograms.
            x (float): Initial x-coordinate in meters.
            y (float): Initial y-coordinate in meters.
            velocity_x (float): Initial velocity in the x-direction in m/s.
            velocity_y (float): Initial velocity in the y-direction in m/s.
        """
        # Parameters
        self.mass = mass
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.time = time
        
        # Logs
        self.x_log = [self.x]
        self.y_log = [self.y]
        self.velocity_x_log = [self.velocity_x]
        self.velocity_y_log = [self.velocity_y]
        self.time_log = [self.time] 
        self.ke_log = [self._kinetic_energy()]
        self.gpe_log = []
        self.total_energy_log = []

    def _kinetic_energy(self) -> float:
        """
        (Private) Calculate the rocket's kinetic energy.

        Returns:
            float: The kinetic energy of the rocket in joules.
        """
        return 0.5 * self.mass * (self.velocity_x**2 + self.velocity_y**2)
    
    def _calculate_gpe(self, G: float, Mass_Earth: float, Mass_Moon: float, Moon_Distance: float) -> float:
        """
        (Private) Calculates the gravitational potential energy of the rocket due to the Earth and optionally the Moon.

        Parameters:
            G (float): Gravitational constant.
            Mass_Earth (float): Mass of the Earth in kilograms.
            Mass_Moon (float): Mass of the Moon in kilograms.
            Moon_Distance (float): Distance of the Moon from the Earth in meters.

        Returns:
            float: Gravitational potential energy (Joules).
        """
        # Calculate the GPE contributions from Earth and Moon
        gpe_earth = -(G * Mass_Earth * self.mass) / math.sqrt((self.x**2) + (self.y**2))
        gpe_moon = -(G * Mass_Moon * self.mass) / math.sqrt(((self.x - Moon_Distance)**2) + (self.y**2))

        # Total GPE
        total_gpe = gpe_earth + gpe_moon
        return total_gpe
    
    def initialize_energies(self, G: float, Mass_Earth: float, Mass_Moon: float, Moon_Distance: float):
        """
        Initialize the gravitational potential energy (GPE) and total energy (TE) logs.

        Parameters:
            G (float): Gravitational constant.
            Mass_Earth (float): Mass of the Earth in kilograms.
            Mass_Moon (float): Mass of the Moon in kilograms.
            Moon_Distance (float): Distance of the Moon from the Earth in meters.
        """
        initial_gpe = self._calculate_gpe(G, Mass_Earth, Mass_Moon, Moon_Distance)
        initial_te = initial_gpe + self.ke_log[0]

        self.gpe_log.append(initial_gpe)
        self.total_energy_log.append(initial_te)
    
    def _acceleration_x(self, G: float, Mass_Earth: float, Mass_Moon: float, x: float, y: float, Moon_Distance: float) -> float:
        """
        (Private) The function uses the gravitational forces of the Earth and the Moon to compute the 
        acceleration in the x direction, based on the rocket's x and y coordinates.

        Parameters:
            G (float): Gravitational constant (m^3 kg^-1 s^-2).
            Mass_Earth (float): Mass of the Earth (kg).
            Mass_Moon (float): Mass of the Moon (kg).
            x (float): x-coordinate of the rocket (m).
            y (float): y-coordinate of the rocket (m).
            Moon_Distance (float): Distance of the Moon from the Earth along the x-axis (m).

        Returns:
            float: The acceleration in the x direction (m/s^2).
        """
        acceleration_x=-((G*Mass_Earth*x)/(((x**2)+(y**2))**(3/2)))-((G*Mass_Moon*(x-Moon_Distance))/(abs(math.sqrt(((x-Moon_Distance)**2)+(y**2)))**3))
        return acceleration_x
    
    def _acceleration_y(self, G: float, Mass_Earth: float, Mass_Moon: float, x: float, y: float, Moon_Distance: float) -> float:
        """
        (Private) The function uses the gravitational forces of the Earth and the Moon to compute the 
        acceleration in the y direction, based on the rocket's x and y coordinates.

        Parameters:
            G (float): Gravitational constant (m^3 kg^-1 s^-2).
            Mass_Earth (float): Mass of the Earth (kg).
            Mass_Moon (float): Mass of the Moon (kg).
            x (float): x-coordinate of the rocket (m).
            y (float): y-coordinate of the rocket (m).
            Moon_Distance (float): Distance of the Moon from the Earth along the x-axis (m).

        Returns:
            float: The acceleration in the y direction (m/s^2).
        """
        acceleration_y=-((G*Mass_Earth*y)/(((x**2)+(y**2))**(3/2)))-((G*Mass_Moon*y)/(abs(math.sqrt(((x-Moon_Distance)**2)+(y**2)))**3))
        return acceleration_y

    def update_position_and_velocity(self, G: float, h: float, Mass_Earth: float, Mass_Moon: float, Moon_Distance: float,  Earth_Radius: float, Moon_Radius: float) -> None:
        """
        Update the rocket's position and velocity using the Runge-Kutta method, and log the changes.

        Parameters:
            G (float): Gravitational constant (m^3 kg^-1 s^-2).
            h (float): Time step (s).
            Mass_Earth (float): Mass of the Earth (kg).
            Mass_Moon (float): Mass of the Moon (kg).
            Moon_Distance (float): Distance of the Moon from the Earth along the x-axis (m).
        """
        # First Runge Kutta evaluations 
        kutta_1x = self.velocity_x
        kutta_1y = self.velocity_y
        kutta_1vx = self._acceleration_x(G, Mass_Earth, Mass_Moon, self.x, self.y, Moon_Distance)
        kutta_1vy = self._acceleration_y(G, Mass_Earth, Mass_Moon, self.x, self.y, Moon_Distance)

        # Second Runge Kutta evaluations 
        kutta_2x = self.velocity_x + (h*kutta_1vx)/2
        kutta_2y = self.velocity_y + (h*kutta_1vy)/2
        a = self.x + (h*kutta_1x)/2
        b = self.y + (h*kutta_1y)/2
        kutta_2vx = self._acceleration_x(G, Mass_Earth, Mass_Moon, a, b, Moon_Distance)
        kutta_2vy = self._acceleration_y(G, Mass_Earth, Mass_Moon, a, b, Moon_Distance)

        # Third Runge Kutta evaluations 
        kutta_3x = self.velocity_x + (h*kutta_2vx)/2
        kutta_3y = self.velocity_y + (h*kutta_2vy)/2
        a = self.x +(h*kutta_2x)/2
        b = self.y + (h*kutta_2y)/2
        kutta_3vx = self._acceleration_x(G, Mass_Earth, Mass_Moon, a, b, Moon_Distance)
        kutta_3vy = self._acceleration_y(G, Mass_Earth, Mass_Moon, a, b, Moon_Distance)

        # Fourth Runge Kutta evaluations 
        kutta_4x = self.velocity_x + (h*kutta_3vx)
        kutta_4y = self.velocity_y + (h*kutta_3vy)
        a = self.x +(h*kutta_3x)
        b = self.y + (h*kutta_3y)       
        kutta_4vx = self._acceleration_x(G, Mass_Earth, Mass_Moon, a, b, Moon_Distance)
        kutta_4vy = self._acceleration_y(G, Mass_Earth, Mass_Moon, a, b, Moon_Distance)

        # Position, velocity, and time updates to be made
        x_plus1 = self.x + ((h/6)*(kutta_1x+(2*kutta_2x)+(2*kutta_3x)+kutta_4x))
        y_plus1 = self.y + ((h/6)*(kutta_1y+(2*kutta_2y)+(2*kutta_3y)+kutta_4y))
        velocity_x_plus1 = self.velocity_x + ((h/6)*(kutta_1vx+(2*kutta_2vx)+(2*kutta_3vx)+kutta_4vx))
        velocity_y_plus1 = self.velocity_y + ((h/6)*(kutta_1vy+(2*kutta_2vy)+(2*kutta_3vy)+kutta_4vy))
        time_plus1 = self.time + h

        # Update parameters 
        self.x = x_plus1
        self.y = y_plus1   
        self.velocity_x = velocity_x_plus1
        self.velocity_y = velocity_y_plus1
        self.time = time_plus1
        
        # Log changes
        self.x_log.append(self.x)
        self.y_log.append(self.y)
        self.velocity_x_log.append(self.velocity_x)
        self.velocity_y_log.append(self.velocity_y)
        self.time_log.append(self.time)

        # Log energies
        ke = self._kinetic_energy()
        gpe = self._calculate_gpe(G, Mass_Earth, Mass_Moon, Moon_Distance)
        self.ke_log.append(ke)
        self.gpe_log.append(gpe)
        self.total_energy_log.append(ke + gpe)

        # Crash detection if position is within Earth or Moon radii
        earth_distance = (self.x**2 + self.y**2)**0.5
        if earth_distance < Earth_Radius:
            raise ValueError("Rocket has crashed into the Earth!")

        if Mass_Moon > 0:  # Check only if Moon is present
            moon_distance = ((self.x - Moon_Distance)**2 + self.y**2)**0.5
            if moon_distance < Moon_Radius:
                raise ValueError("Rocket has crashed into the Moon!")

    def __repr__(self) -> str:
        """
        Return a string representation of the rocket's current state.

        Returns:
            str: A string summarizing the rocket's mass, position, and velocity.
        """
        return (f"Rocket(mass={self.mass}, x={self.x:.2f}, y={self.y:.2f}, "
                f"velocity_x={self.velocity_x:.2f}, velocity_y={self.velocity_y:.2f})")
        

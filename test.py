from rocket.py import Rocket
from planet.py import Planet
from planet_constants import G, EARTH_MASS, EARTH_RADIUS

earth = Planet('Earth', EARTH_MASS, EARTH_RADIUS)
rocket = Rocket(100, 0, 7E6, 7543, 0, 0)

time_target = 5000
h = 10

#for rocket.time_log[-1] in < time_target:
 #   rocket.update_position_and_velocity(G, h, EARTH_MASS, 0, 0)



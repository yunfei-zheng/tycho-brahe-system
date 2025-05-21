# ===========================================
# - Tycho Brahe's System of the Universe Simulation
# - Yunfei Zheng, etc ---
# - Understanding the Universe: From Atoms to the Big Bang (SP25)
# - February 2025
# ===========Modified From===================
# - Title:  Solar System Simulation
# - Author: @zerot69
# - Date:   27 Apr 2022
# ===========================================

# TODO:
# The current calculations for the orbits seem to make it shift down, and move,
#  but we can probably just do fixed orbits.
# Add new features, like speeding up or slowing down
# maybe make the planets sizes bigger

import pygame
import math

pygame.init()
WIDTH, HEIGHT = 400, 400
WINDOW = pygame.display.set_mode((800,800))

# Colors of planets and universe
COLOR_WHITE = (255, 255, 255)
COLOR_UNIVERSE = (36, 36, 36)
COLOR_SUN = (252, 150, 1)
COLOR_VENUS = (227, 158, 28)
COLOR_EARTH = (107, 147, 214)

# Definite circulator 
# Ellisipe travel certain angle per time
# 1 Year timeline 

# Each planet need mass, 


#  k =  speed
# a  = time variablt 
EARTH_POSITION = WIDTH/2, HEIGHT/2
SUN_DISTANCE_FROM_EARTH = 100 

def position( radius, orbit_speed, time, init_angle ):
    x = SUN_DISTANCE_FROM_EARTH(math.cos(time ) + radius(math.cos(orbit_speed * time + init_angle)))
    y = SUN_DISTANCE_FROM_EARTH(math.sin(time) + radius(math.sin(orbit_speed * time + init_angle)))
    return x,y



class PlanetAndEpicycles: 
    AU = 149.6e6 * 1000  # Astronomical unit
    G = 6.67428e-11  # Gravitational constant
    TIMESTEP = 60 * 60 * 24 * 2  # Seconds in 2 days
    SCALE = 200 / AU
    
    def __init__(self, radius, color, mass, angle) :
        self.radius = radius # use this to draw planet, highlight the rotation too 
        self.color = color
        self.mass = mass
        self.angle = angle # rotation of Epicyles
        self.distance_to_sun = 0 # maybe make this a input for simplicity 
        
    def draw(self,window): 
        

def main():
    run = True
    pause = False
    pygame.quit()

if __name__ == "__main__":
    main()
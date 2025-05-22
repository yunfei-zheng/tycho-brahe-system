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
COLOR_VENUS = (80, 200, 120)  # soft, vibrant green
COLOR_EARTH = (107, 147, 214)

# Definite circulator 
# Ellisipe travel certain angle per time
# 1 Year timeline 

# Each planet need mass, 


#  k =  speed
# a  = time variablt 
EARTH_POSITION = WIDTH/2, HEIGHT/2
SUN_DISTANCE_FROM_EARTH = 100 

def sun_position(radius, orbit_speed, time, init_angle):
    x = WIDTH/2 + SUN_DISTANCE_FROM_EARTH*(math.cos(time) + radius*(math.cos(orbit_speed * time + init_angle)))
    y = HEIGHT/2 + SUN_DISTANCE_FROM_EARTH*(math.sin(time) + radius*(math.sin(orbit_speed * time + init_angle)))
    return x, y
def planet_position(radius, orbit_speed, time, init_angle, distance_from_sun):
    sun_x, sun_y = sun_position(radius, orbit_speed, time, init_angle)
    x = sun_x + distance_from_sun * math.cos(orbit_speed * time + init_angle)
    y = sun_y + distance_from_sun * math.sin(orbit_speed * time + init_angle)
    return x, y


class PlanetAndEpicycles: 
    AU = 149.6e6 * 1000  # Astronomical unit
    G = 6.67428e-11  # Gravitational constant
    TIMESTEP = 60 * 60 * 24 * 2  # Seconds in 2 days
    SCALE = 200 / AU
    
    def __init__(self, color, orbit_speed, init_angle, time, radius, distance_from_sun, is_sun=False):
        self.x = WIDTH/2  # Initialize at center
        self.y = HEIGHT/2
        self.orbit_speed = orbit_speed
        self.init_angle = init_angle
        self.time = time
        self.radius = radius
        self.color = color
        self.is_sun = is_sun
        self.sun_x = WIDTH/2
        self.sun_y = HEIGHT/2
        self.distance_from_sun = distance_from_sun
    def draw(self, window, draw_line):
        if self.is_sun:
            # Sun orbits around Earth
            self.x, self.y = sun_position(0, self.orbit_speed, self.time, self.init_angle,)
            pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)
        else:
            # Other planets orbit around Sun
            # Then calculate planet's position relative to Sun
            self.x, self.y = planet_position(self.radius, self.orbit_speed, self.time, self.init_angle, self.distance_from_sun)
            if draw_line:
                pygame.draw.lines(window, self.color, False, [(self.sun_x, self.sun_y), (self.x, self.y)], 1)
            pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)
    
    def update_position(self, time):
        self.time = time  # Update the time property

def draw_earth(window):
    # Draw Earth at the center
    pygame.draw.circle(window, COLOR_EARTH, (WIDTH//2, HEIGHT//2), 15)

def main():
    run = True
    pause = False
    show_distance = False
    clock = pygame.time.Clock()
    real_time = 0
    last_reported_second = -1
    
    sun = PlanetAndEpicycles(COLOR_SUN, 0.001, 0, 0, 20, 0, is_sun=True)  # Sun orbiting Earth
    venus = PlanetAndEpicycles(COLOR_VENUS, 0.006, 0, 0, 5, 0, is_sun=False)  # Venus orbiting Sun
    draw_line = True
    
    planets = [sun, venus]

    while run:
        dt = clock.tick(60) / 1000  # convert milliseconds to seconds
        real_time += dt

        # Round down to the nearest full second
        current_second = math.floor(real_time)

        # Only print once per new second
        if current_second > last_reported_second:
            last_reported_second = current_second
            print(f"{current_second} seconds")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Clear the screen
        WINDOW.fill(COLOR_UNIVERSE)
        
        # Draw Earth first (it's stationary)
        draw_earth(WINDOW)
        
        # Draw and update planets
        for planet in planets:
            if not pause:
                planet.update_position(real_time)
                planet.draw(WINDOW, draw_line)
        
        # Update the display
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
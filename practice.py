# ===========================================
# - Tycho Brahe's System of the Universe Simulation
# - Yunfei Zheng, Joyce Zou, Minh Nguyen ---
# - Understanding the Universe: From Atoms to the Big Bang (SP25)
# - May 2025
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
# Don't need to divide these by 2, it already accounts for it
WIDTH, HEIGHT = 400, 400
WINDOW = pygame.display.set_mode((800,800))

# Constants: Colors of planets and universe
COLOR_WHITE = (255, 255, 255)
COLOR_UNIVERSE = (36, 36, 36)
COLOR_EARTH = (107, 147, 214)
COLOR_SUN = (252, 150, 1)
COLOR_VENUS = (80, 200, 120)  # soft, vibrant green

FONT_1 = pygame.font.SysFont("Trebuchet MS", 21)
FONT_2 = pygame.font.SysFont("Trebuchet MS", 16)

SUN_DISTANCE_FROM_EARTH = 200

SUN_X, SUN_Y = WIDTH, HEIGHT

# Definite circulator 
# Ellipse travel certain angle per time
# 1 Year timeline 

# Each planet need mass, 
# k = speed
# a = time variable

# Removed *sc
def sun_position(radius, orbit_speed, time, init_angle):
    sc = PlanetAndEpicycles.SCALE
    x = WIDTH + SUN_DISTANCE_FROM_EARTH*(math.cos(time) + radius*(math.cos(orbit_speed * time + init_angle)))
    y = HEIGHT + SUN_DISTANCE_FROM_EARTH*(math.sin(time) + radius*(math.sin(orbit_speed * time + init_angle)))

    PlanetAndEpicycles.sun_x = x
    PlanetAndEpicycles.sun_y = y

    return x, y

def planet_position(orbit_speed, time, init_angle, distance_from_sun):
    sun_x, sun_y = PlanetAndEpicycles.sun_x, PlanetAndEpicycles.sun_y
    sc = PlanetAndEpicycles.SCALE

    x = sun_x + sc*distance_from_sun * math.cos(orbit_speed * time + init_angle)
    y = sun_y + sc*distance_from_sun * math.sin(orbit_speed * time + init_angle)

    return x, y

class PlanetAndEpicycles: 
    AU = 149.6e6 * 1000  # Astronomical unit to km
    G = 6.67428e-11  # Gravitational constant
    TIMESTEP = 60 * 60 * 24 * 2  # Seconds in 2 days
    #SCALE = 200 / AU
    SCALE = 1

    sun_x = 0
    sun_y = 0
    
    def __init__(self, color, orbit_speed, init_angle, radius, distance_from_sun, is_sun):
        self.x = WIDTH  # Initialize at center
        self.y = HEIGHT
        self.orbit = []
        self.orbit_speed = orbit_speed
        self.init_angle = init_angle
        self.time = 0
        self.radius = radius
        self.color = color
        self.is_sun = is_sun
        self.sun_x = WIDTH
        self.sun_y = HEIGHT
        self.distance_from_sun = distance_from_sun

    def draw(self, window, draw_line):
        camera_x, camera_y = earth.x, earth.y
        x = (self.x - camera_x) * self.SCALE + center_x
        y = (self.y - camera_y) * self.SCALE + center_y

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                px, py = point
                x = (px - camera_x) * self.SCALE + center_x
                y = (py - camera_y) * self.SCALE + center_y
                #updated_points.append((x + move_x, y + move_y))
                updated_points.append((x, y))
            if draw_line:
                pygame.draw.lines(window, self.color, False, updated_points, 1)
        if self.is_sun:
            # Sun orbits around Earth
            self.x, self.y = sun_position(0, self.orbit_speed, self.time, self.init_angle)
            SUN_X, SUN_Y = self.x, self.y
            # Store globally 
            pygame.draw.circle(window, self.color, (int(x), int(y)), int(self.radius * self.SCALE))
        else:
            # Other planets orbit around Sun
            # Then calculate planet's position relative to Sun
            self.x, self.y = planet_position(self.orbit_speed, self.time, self.init_angle, self.distance_from_sun)
            pygame.draw.circle(window, self.color, (int(x), int(y)), int(self.radius * self.SCALE))
    
    def update_position(self, time):
        self.time = time  # Update the time property
        # So it doesn't count starting point?
        self.orbit.append((self.x, self.y))

    def update_scale(self, scale):
        # self.radius *= scale
        pass
    
earth = PlanetAndEpicycles(COLOR_EARTH, 0, 0, 15, 0, False)
earth.x = 0  # origin
earth.y = 0
center_x, center_y = WIDTH/2, HEIGHT/2
camera_x, camera_y = earth.x, earth.y


def draw_earth(window, sun_x, sun_y):
    pygame.draw.circle(window, COLOR_EARTH, (sun_x, sun_y), int(15 * PlanetAndEpicycles.SCALE))
def main():
    run = True
    pause = False #(Doesn't work rn)
    show_distance = False
    clock = pygame.time.Clock()
    real_time = 0
    #last_reported_second = -1
    draw_line = True
    
    #( color, orbit_speed, init_angle, radius, distance_from_sun, is_sun=False):
    sun = PlanetAndEpicycles(COLOR_SUN, 0.001, 0, 20, 0, True)  # Sun orbiting Earth
    venus = PlanetAndEpicycles(COLOR_VENUS, 6, 20, 5, 30, False)  # Venus orbiting Sun
    
    planets = [sun, venus]

    while run:
        dt = clock.tick(60) / 1000  # convert milliseconds to seconds
        real_time += dt

        # Round down to the nearest full second
        #current_second = math.floor(real_time)
        # Only print once per new second
        #if current_second > last_reported_second:
            #last_reported_second = current_second
            #print(f"{current_second} seconds")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                (event.key == pygame.K_x or event.key == pygame.K_ESCAPE)):
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                draw_line = not draw_line
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                PlanetAndEpicycles.SCALE *= 0.75
                for planet in planets:
                    planet.update_scale(0.75)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                PlanetAndEpicycles.SCALE *= 1.25
                for planet in planets:
                    planet.update_scale(1.25)
            # elif event.type == pygame.MOUSEWHEEL:
                
                    
        
        # Clear the screen
        WINDOW.fill(COLOR_UNIVERSE)

        # Removed move_x, move_y and camera movement handling

        # Draw Earth first (it's stationary)
        draw_earth(WINDOW, SUN_X, SUN_Y)
        
        # Draw and update planets
        for planet in planets:
            if not pause:
                planet.update_position(real_time)
                planet.draw(WINDOW, draw_line)
        
        # Rendering the text, map legend, etc.
        fps_text = FONT_1.render("FPS: " + str(int(clock.get_fps())), True, COLOR_WHITE)
        WINDOW.blit(fps_text, (15, 15))
        text_surface = FONT_1.render("Press X or ESC to exit", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 45))
        text_surface = FONT_1.render("Press S to turn on/off drawing orbit lines", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 105))
        text_surface = FONT_1.render("Use scroll-wheel to zoom", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 225))

        sun_surface = FONT_1.render("- Sun", True, COLOR_SUN)
        WINDOW.blit(sun_surface, (15, 285))

        venus_surface = FONT_1.render("- Venus", True, COLOR_VENUS)
        WINDOW.blit(venus_surface, (15, 345))

        earth_surface = FONT_1.render("- Earth", True, COLOR_EARTH)
        WINDOW.blit(earth_surface, (15, 375))

        # Update the display
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
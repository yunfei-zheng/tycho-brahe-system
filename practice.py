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

EARTH_POSITION = WIDTH/2, HEIGHT/2
SUN_DISTANCE_FROM_EARTH = 200

# Definite circulator 
# Ellipse travel certain angle per time
# 1 Year timeline 

# Each planet need mass, 
# k = speed
# a = time variable

def sun_position(radius, orbit_speed, time, init_angle):
    sc = PlanetAndEpicycles.SCALE
    x = WIDTH + sc*SUN_DISTANCE_FROM_EARTH*(math.cos(time) + radius*(math.cos(orbit_speed * time + init_angle)))
    y = HEIGHT + sc*SUN_DISTANCE_FROM_EARTH*(math.sin(time) + radius*(math.sin(orbit_speed * time + init_angle)))

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

    def draw(self, window, move_x, move_y, draw_line):
        x = self.x * self.SCALE
        y = self.y * self.SCALE

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE
                y = y * self.SCALE
                #updated_points.append((x + move_x, y + move_y))
                updated_points.append((x + move_x, y + move_y))
            if draw_line:
                pygame.draw.lines(window, self.color, False, updated_points, 1)
        if self.is_sun:
            # Sun orbits around Earth
            self.x, self.y = sun_position(0, self.orbit_speed, self.time, self.init_angle)
            pygame.draw.circle(window, self.color, (x + move_x, y + move_y), self.radius)
        else:
            # Other planets orbit around Sun
            # Then calculate planet's position relative to Sun
            self.x, self.y = planet_position(self.orbit_speed, self.time, self.init_angle, self.distance_from_sun)
            pygame.draw.circle(window, self.color, (x + move_x, y + move_y), self.radius)
    
    def update_position(self, time):
        self.time = time  # Update the time property
        # So it doesn't count starting point?
        self.orbit.append((self.x, self.y))

    def update_scale(self, scale):
        self.radius *= scale

def draw_earth(window, move_x, move_y):
    # Draw Earth at the center
    #sc = PlanetAndEpicycles.SCALE
    pygame.draw.circle(window, COLOR_EARTH, (WIDTH + move_x, HEIGHT + move_y), 15 * PlanetAndEpicycles.SCALE)

def main():
    run = True
    pause = False #(Doesn't work rn)
    show_distance = False
    clock = pygame.time.Clock()
    real_time = 0
    #last_reported_second = -1
    move_x = 0
    move_y = 0
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
        
        # Clear the screen
        WINDOW.fill(COLOR_UNIVERSE)

        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        window_w, window_h = pygame.display.get_surface().get_size()
        distance = 10
        if keys[pygame.K_LEFT] or mouse_x == 0:
            move_x += distance
        if keys[pygame.K_RIGHT] or mouse_x == window_w - 1:
            move_x -= distance
        if keys[pygame.K_UP] or mouse_y == 0:
            move_y += distance
        if keys[pygame.K_DOWN] or mouse_y == window_h - 1:
            move_y -= distance
        
        # Draw Earth first (it's stationary)
        draw_earth(WINDOW, move_x, move_y)
        
        # Draw and update planets
        for planet in planets:
            if not pause:
                planet.update_position(real_time)
                planet.draw(WINDOW, move_x, move_y, draw_line)
        
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
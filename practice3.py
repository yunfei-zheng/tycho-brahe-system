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

# Initialize Pygame
pygame.init()

# Screen dimensions and center
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
CENTER_X, CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tycho Brahe Solar System")

# Colors
COLOR_BG     = (36, 36, 36)
COLOR_EARTH  = (107, 147, 214)
COLOR_SUN    = (252, 150,   1)
COLOR_VENUS  = ( 80, 200, 120)
COLOR_MARS   = (255, 0, 0)
COLOR_WHITE  = (255, 255, 255)

# Font
FONT = pygame.font.SysFont("Trebuchet MS", 20)

# Distances (in pixels)
SUN_DIST = 200  # Sun orbits Earth at this radius

class Body:
    SCALE = 1.0  # global scale factor for zoom
    sun_world = (0.0, 0.0)  # world coords of Sun

    def __init__(self, color, speed, init_angle, radius, dist_from_sun, is_sun=False):
        self.color = color
        self.speed = speed
        self.angle = init_angle
        self.radius = radius
        self.dist = dist_from_sun
        self.is_sun = is_sun
        self.trail = []  # stores past world positions

    def update(self, dt):
        # advance angular position
        self.angle += self.speed * dt
        # compute world coords
        if self.is_sun:
            # Sun orbits Earth
            wx = SUN_DIST * math.cos(self.angle)
            wy = SUN_DIST * math.sin(self.angle)
            Body.sun_world = (wx, wy)
        else:
            # planet orbits Sun's world position
            sx, sy = Body.sun_world
            wx = sx + self.dist * math.cos(self.angle)
            wy = sy + self.dist * math.sin(self.angle)
        self.trail.append((wx, wy))
        # limit trail length
        if len(self.trail) > 3600:
            self.trail.pop(0)
        self.world = (wx, wy)

    def draw(self, surf, offset_x, offset_y):
        # draw trail
        if len(self.trail) > 2:
            pts = [(
                int(CENTER_X + px * Body.SCALE + offset_x),
                int(CENTER_Y + py * Body.SCALE + offset_y)
            ) for px, py in self.trail]
            pygame.draw.lines(surf, self.color, False, pts, 1)
        # draw body
        if not self.is_sun:
            # draw epicycle path circle around Sun
            sx_sun = int(CENTER_X + Body.sun_world[0] * Body.SCALE + offset_x)
            sy_sun = int(CENTER_Y + Body.sun_world[1] * Body.SCALE + offset_y)
            pygame.draw.circle(surf, self.color, (sx_sun, sy_sun), int(self.dist * Body.SCALE), 1)
        wx, wy = self.world
        sx = int(CENTER_X + wx * Body.SCALE + offset_x)
        sy = int(CENTER_Y + wy * Body.SCALE + offset_y)
        pygame.draw.circle(surf, self.color, (sx, sy), int(self.radius * Body.SCALE))

def draw_earth(surf, ox, oy):
    pygame.draw.circle(
        surf, COLOR_EARTH,
        (CENTER_X + ox, CENTER_Y + oy),
        int(15 * Body.SCALE)
    )
    

AU_PIXELS = 200
# Orbital periods (in days)
T_sun   = 365.25    # Sun’s “orbit” around Earth
T_venus = 224.70
T_mars  = 686.98

seconds_per_day = 24*60*60 
# Convert to radians per day
ω_sun_per_day   = 2*math.pi / T_sun
ω_venus_per_day = 2*math.pi / T_venus
ω_mars_per_day  = 2*math.pi / T_mars


ω_sun   = ω_sun_per_day   / seconds_per_day
ω_venus = ω_venus_per_day / seconds_per_day
ω_mars  = ω_mars_per_day  / seconds_per_day

# === real-time mapping: 1 minute per Sun orbit ===
SIMULATION_PERIOD = 5.0  # seconds for one full Sun–Earth revolution
ω_sun   = 2 * math.pi / SIMULATION_PERIOD
# keep true ratio of orbital periods
ω_venus = ω_sun * (T_sun   / T_venus)
ω_mars  = ω_sun * (T_sun   / T_mars)



def main():
    clock = pygame.time.Clock()
    running = True
    offset_x = offset_y = 0
    draw_trails = True

    # create bodies (use per-day angular speeds for visual update)
    sun   = Body(COLOR_SUN,   ω_sun,   init_angle=0.0,           radius=20, dist_from_sun=AU_PIXELS, is_sun=True)
    venus = Body(COLOR_VENUS, ω_venus, init_angle=math.radians(45), radius=8,  dist_from_sun=int(0.723*AU_PIXELS))
    mars  = Body(COLOR_MARS,  ω_mars,  init_angle=math.radians(90), radius=6,  dist_from_sun=int(1.524*AU_PIXELS))
    bodies = [sun, venus, mars]


    while running:
        dt = clock.tick(60) / 1000.0
        # convert frame time to days for angular update
        # dt_days = dt / seconds_per_day
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_x, pygame.K_ESCAPE): running = False
                if e.key == pygame.K_s: draw_trails = not draw_trails
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # zoom
                if e.button == 4: Body.SCALE *= 1.1
                if e.button == 5: Body.SCALE *= 0.9

        # pan with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  offset_x += 5
        if keys[pygame.K_RIGHT]: offset_x -= 5
        if keys[pygame.K_UP]:    offset_y += 5
        if keys[pygame.K_DOWN]:  offset_y -= 5

        # update positions (dt_days is in days)
        for b in bodies:
            b.update(dt)

        # draw
        screen.fill(COLOR_BG)
        draw_earth(screen, offset_x, offset_y)
        for b in bodies:
            if draw_trails: b.draw(screen, offset_x, offset_y)
            else:
                # draw without trails
                wx, wy = b.world
                sx = int(CENTER_X + wx * Body.SCALE + offset_x)
                sy = int(CENTER_Y + wy * Body.SCALE + offset_y)
                pygame.draw.circle(screen, b.color, (sx, sy), int(b.radius * Body.SCALE))

        # UI text
        fps = FONT.render(f"FPS: {int(clock.get_fps())}", True, COLOR_WHITE)
        screen.blit(fps, (10, 10))
        instr = FONT.render("Arrows to pan, Scroll to zoom, S to toggle trails", True, COLOR_WHITE)
        screen.blit(instr, (10, 40))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

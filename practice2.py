
# ===========================================
# - Tycho Brahe's Geocentric Solar System Simulation
# - Yunfei Zheng, Joyce Zou, Minh Nguyen ---
# - Understanding the Universe: From Atoms to the Big Bang (SP25)
# - May 2025
# ===========Modified From===================
# - Title:  Solar System Simulation
# - Author: @zerot69
# - Date:   27 Apr 2022
# ===========================================

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
COLOR_BG      = (36, 36, 36)
COLOR_EARTH   = (107, 147, 214)
COLOR_SUN     = (252, 150,   1)
COLOR_MOON    = (200, 200, 200)
COLOR_MERCURY = (169, 169, 169)
COLOR_VENUS   = ( 80, 200, 120)
COLOR_MARS    = (188,  39,  50)
COLOR_JUPITER = (205, 133,  63)
COLOR_SATURN  = (210, 180, 140)
COLOR_WHITE   = (255, 255, 255)

# Font
FONT = pygame.font.SysFont("Trebuchet MS", 20)

# Distances (in pixels)
SUN_DIST        = 500  # Increased: Sun orbits Earth at this radius
MOON_DIST       = 60   # Moon orbits Earth
MERCURY_DIST    = 100
VENUS_DIST      = 150
MARS_DIST       = 200
JUPITER_DIST    = 275
SATURN_DIST     = 325

class Body:
    SCALE = 1.0  # zoom
    sun_world = (0.0, 0.0)  # sun position in world coords

    def __init__(self, label, color, speed, init_angle, radius, dist, kind='planet'):
        self.label = label
        self.color = color
        self.speed = speed
        self.angle = init_angle
        self.radius = radius
        self.dist = dist
        self.kind = kind  # 'sun', 'moon', or 'planet'
        self.trail = []
        self.world = (0.0, 0.0)

    def update(self, dt):
        self.angle += self.speed * dt
        # world coords
        if self.kind == 'sun':
            wx = SUN_DIST * math.cos(self.angle)
            wy = SUN_DIST * math.sin(self.angle)
            Body.sun_world = (wx, wy)
        elif self.kind == 'moon':
            wx = MOON_DIST * math.cos(self.angle)
            wy = MOON_DIST * math.sin(self.angle)
        else:
            sx, sy = Body.sun_world
            wx = sx + self.dist * math.cos(self.angle)
            wy = sy + self.dist * math.sin(self.angle)
        self.world = (wx, wy)
        self.trail.append(self.world)
        if len(self.trail) > 300:
            self.trail.pop(0)

    def draw(self, surf, ox, oy, show_trail=True, show_label=True):
        # trail
        if show_trail and len(self.trail) > 2:
            pts = [(
                int(CENTER_X + px * Body.SCALE + ox),
                int(CENTER_Y + py * Body.SCALE + oy)
            ) for px, py in self.trail]
            pygame.draw.lines(surf, self.color, False, pts, 1)
        # body
        wx, wy = self.world
        sx = int(CENTER_X + wx * Body.SCALE + ox)
        sy = int(CENTER_Y + wy * Body.SCALE + oy)
        pygame.draw.circle(surf, self.color, (sx, sy), int(self.radius * Body.SCALE))
        # label
        if show_label:
            screen.blit(FONT.render(self.label, True, COLOR_WHITE), (sx, sy))


def draw_earth(surf, ox, oy, show_label=True):
    pygame.draw.circle(
        surf, COLOR_EARTH,
        (CENTER_X + ox, CENTER_Y + oy),
        int(15 * Body.SCALE)
    )
    if show_label:
        screen.blit(FONT.render("Earth", True, COLOR_WHITE), (CENTER_X + ox, CENTER_Y + oy))


def main():
    clock = pygame.time.Clock()
    running = True
    ox = oy = 0
    show_labels = True
    show_trails = True
    timescale = 1
    active = 7 # 7 is all, 2-6 are Mercury-Saturn (index in bodies)

    # create bodies: sun, moon, and planets
    sun     = Body("Sun", COLOR_SUN,     0.5,  0.0, 20,    0, kind='sun')
    moon    = Body("Moon", COLOR_MOON,    2.0,  math.radians(0), 6, 0, kind='moon')
    mercury = Body("Mercury", COLOR_MERCURY, 3.0,  math.radians(0), 5, MERCURY_DIST)
    venus   = Body("Venus", COLOR_VENUS,   2.5,  math.radians(45), 7, VENUS_DIST)
    mars    = Body("Mars", COLOR_MARS,    1.8,  math.radians(90), 6, MARS_DIST)
    jupiter = Body("Jupiter", COLOR_JUPITER, 1.2,  math.radians(135),12, JUPITER_DIST)
    saturn  = Body("Saturn", COLOR_SATURN,  0.8,  math.radians(180),10, SATURN_DIST)
    bodies = [sun, moon, mercury, venus, mars, jupiter, saturn]

    while running:
        dt = clock.tick(60) / 1000.0 * timescale
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_x, pygame.K_ESCAPE): running = False
                if e.key == pygame.K_a: active = 2 if active == 7 else active + 1
                if e.key == pygame.K_l: show_labels = not show_labels
                if e.key == pygame.K_s: show_trails = not show_trails
                if e.key == pygame.K_j: timescale *= 0.5
                if e.key == pygame.K_k: timescale *= 2
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4: Body.SCALE *= 1.1
                if e.button == 5: Body.SCALE *= 0.9

        # pan
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  ox += 5
        if keys[pygame.K_RIGHT]: ox -= 5
        if keys[pygame.K_UP]:    oy += 5
        if keys[pygame.K_DOWN]:  oy -= 5

        # update and draw
        screen.fill(COLOR_BG)
        draw_earth(screen, ox, oy, show_labels)
        for n, b in enumerate(bodies):
            b.update(dt)
            if active == 7:
                b.draw(screen, ox, oy, show_trails, show_labels)
            # Only draw sun, moon, and active planet
            elif n < 2 or active == n:
                b.draw(screen, ox, oy, show_trails, show_labels)

        # UI
        screen.blit(FONT.render(f"FPS: {int(clock.get_fps())}", True, COLOR_WHITE), (10, 10))
        screen.blit(FONT.render("Arrows to pan, Scroll to zoom, A to focus on one planet", True, COLOR_WHITE), (10, 40))
        screen.blit(FONT.render("S: Toggle trails, J/K: Slow down/speed up, L: Toggle labels", True, COLOR_WHITE), (10, 70))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

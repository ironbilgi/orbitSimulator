import math
import pygame


class Planet:

    def __init__(self, name, mass, radius, color, orbit_radius, orbit_speed, orbit_angle, trail, orbit_path):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.color = color
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.orbit_angle = orbit_angle
        self.trail = [] if trail else None
        self.orbit_path = orbit_path if orbit_path else None

    def update_position(self, dt):
        self.orbit_angle += self.orbit_speed * dt

    def get_position(self, center_x, center_y):
        x = center_x + self.orbit_radius * math.cos(self.orbit_angle)
        y = center_y + self.orbit_radius * math.sin(self.orbit_angle)
        return (x, y)

    def draw(self, screen, center_x, center_y):
        x, y = self.get_position(center_x, center_y)

        if self.trail is not None:
            self.trail.append((x, y))
            if len(self.trail) > 100:  # Limit trail length
                self.trail.pop(0)

            for i in range(1, len(self.trail)):
                start = self.trail[i - 1]
                end = self.trail[i]
                pygame.draw.line(screen, (120, 120, 140), start, end, 1)
        if self.orbit_path is not None:
            pygame.draw.circle(screen, (80, 80, 100), (center_x, center_y), self.orbit_radius, 1)

        pygame.draw.circle(screen, self.color, (int(x), int(y)), self.radius)

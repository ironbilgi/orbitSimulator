import math
import pygame


class Planet:

    def __init__(self, name, mass, radius, color, orbit_radius, orbit_speed, orbit_angle):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.color = color
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.orbit_angle = orbit_angle

    def update_position(self, dt):
        self.orbit_angle += self.orbit_speed * dt

    def get_position(self, center_x, center_y):
        x = center_x + self.orbit_radius * math.cos(self.orbit_angle)
        y = center_y + self.orbit_radius * math.sin(self.orbit_angle)
        return (x, y)

    def draw(self, screen, center_x, center_y):
        x, y = self.get_position(center_x, center_y)
        pygame.draw.circle(screen, self.color, (int(x), int(y)), self.radius)

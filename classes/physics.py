import pygame

class OrbitalPhysics:
    def __init__(self, gravitational_constant=0.5):
        """Initializes the physics engine with a universe scale factor (G)."""
        self.G = gravitational_constant

    def calculate_gravity_acceleration(self, body_pos, planet_pos, planet_mass):
        """
        Applies Newton's Law of Universal Gravitation math.
        Returns a Vector2 representing the acceleration pull for this frame.
        """
        # 1. Distance Math: Get the vector pointing from body to planet
        direction = planet_pos - body_pos
        distance = direction.length()
        
        # Crash safety: stop pulling if objects overlap to prevent infinite force glitches
        if distance < 10:
            return pygame.math.Vector2(0, 0)
            
        # 2. Direction Math: Normalize the vector to get a unit vector (length of 1)
        direction_normalized = direction.normalize()
        
        # 3. Force Math: F = (G * M) / r^2
        force_magnitude = (self.G * planet_mass) / (distance ** 2)
        
        # 4. Return the final acceleration vector
        return direction_normalized * force_magnitude

    def update_body(self, body_pos, body_vel, planet_pos, planet_mass):
        """
        Updates a body's position and velocity for the current real frame.
        Modifies and returns the updated (position, velocity) vectors.
        """
        acceleration = self.calculate_gravity_acceleration(body_pos, planet_pos, planet_mass)
        
        # Step velocity, then step position (Euler Integration)
        body_vel += acceleration
        body_pos += body_vel
        
        return body_pos, body_vel

    def get_orbit_projection(self, ship_pos, ship_vel, planet_pos, planet_mass, steps=250,
                              planet_radius=50, ship_radius=0, escape_distance=2000):
        """
        Runs a fast 'virtual' physics loop into the future.
        Returns a tuple of (points, status), where points is a list of (x, y)
        integer tuples for Pygame to draw as a line, and status is one of
        "orbiting", "crashed", or "escaped".
        """
        projection_points = []
        status = "orbiting"

        # Clone current vectors so we don't manipulate the active ship
        virtual_pos = pygame.math.Vector2(ship_pos)
        virtual_vel = pygame.math.Vector2(ship_vel)

        for _ in range(steps):
            acceleration = self.calculate_gravity_acceleration(virtual_pos, planet_pos, planet_mass)
            virtual_vel += acceleration
            virtual_pos += virtual_vel

            # Store point as simple tuple for quick Pygame rendering
            projection_points.append((int(virtual_pos.x), int(virtual_pos.y)))

            distance = (planet_pos - virtual_pos).length()
            if distance <= planet_radius + ship_radius:
                status = "crashed"
                break
            if distance > escape_distance:
                status = "escaped"
                break

        return projection_points, status
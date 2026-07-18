import pygame


class Dropdown:
    """A simple dropdown menu for choosing an option."""

    def __init__(self, x, y, width, height, options, default_index=0, data=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.data = data or {}  # Dictionary to store additional data like mass
        self.selected_index = default_index
        self.open = False
        self.selection_made = False

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        main_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if main_rect.collidepoint(mouse_x, mouse_y):
            self.open = not self.open
            return

        if self.open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.x,
                    self.y + self.height + i * self.height,
                    self.width,
                    self.height,
                )
                if option_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_index = i
                    self.open = False
                    self.selection_made = True
                    return

            self.open = False

    def draw(self, screen, font):
        main_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 255, 255), main_rect)
        pygame.draw.rect(screen, (0, 0, 0), main_rect, 2)

        text = font.render(self.options[self.selected_index], True, (0, 0, 0))
        screen.blit(text, (self.x + 10, self.y + 8))

        if self.open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.x,
                    self.y + self.height + i * self.height,
                    self.width,
                    self.height,
                )
                pygame.draw.rect(screen, (240, 240, 240), option_rect)
                pygame.draw.rect(screen, (0, 0, 0), option_rect, 1)

                option_text = font.render(option, True, (0, 0, 0))
                screen.blit(option_text, (self.x + 10, self.y +
                            self.height + i * self.height + 8))

    def get_selected(self):
        return self.options[self.selected_index]

    def has_selection(self):
        return self.selection_made

    def get_data(self, key=None):
        """Get data for the selected option."""
        selected = self.get_selected()
        if selected in self.data:
            if key is None:
                return self.data[selected]
            return self.data[selected].get(key)


class Slider:
    """A simple horizontal slider for pygame projects."""

    def __init__(self, x, y, width, height=20, min_value=0, max_value=100, value=50):
        # Step 1: Store the slider's position and size.
        # These numbers control where the slider appears on the screen.
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Step 2: Store the minimum and maximum values.
        # The slider can only move between these two numbers.
        self.min_value = min_value
        self.max_value = max_value

        # Step 3: Store the current value.
        # This is the value the slider is currently set to.
        self.value = value

        # Step 4: Choose colors for the bar and handle.
        self.bar_color = (180, 180, 180)
        self.handle_color = (70, 130, 180)
        self.border_color = (40, 40, 40)

        # Step 5: Set the knob size.
        self.handle_radius = 12

        # Step 6: Track whether the user is dragging the handle.
        self.dragging = False

    def _get_handle_x(self):
        # Step 7: Convert the current value into a horizontal position.
        if self.max_value == self.min_value:
            return self.x

        ratio = (self.value - self.min_value) / \
            (self.max_value - self.min_value)
        return self.x + ratio * self.width

    def draw(self, screen):
        # Step 8: Draw the slider bar.
        bar_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.bar_color, bar_rect)
        pygame.draw.rect(screen, self.border_color, bar_rect, 2)

        # Step 9: Find the handle position from the current value.
        handle_x = self._get_handle_x()
        handle_y = self.y + self.height // 2

        # Step 10: Draw the circular handle.
        pygame.draw.circle(screen, self.handle_color,
                           (int(handle_x), handle_y), self.handle_radius)
        pygame.draw.circle(screen, self.border_color,
                           (int(handle_x), handle_y), self.handle_radius, 2)

    def _update_from_mouse(self, mouse_x):
        # Move the slider value based on the mouse position.
        if mouse_x < self.x:
            mouse_x = self.x
        elif mouse_x > self.x + self.width:
            mouse_x = self.x + self.width

        if self.width <= 0:
            ratio = 0
        else:
            ratio = (mouse_x - self.x) / self.width

        self.value = self.min_value + ratio * (self.max_value - self.min_value)

        if self.value < self.min_value:
            self.value = self.min_value
        elif self.value > self.max_value:
            self.value = self.max_value

    def handle_event(self, event):
        # Step 11: Check if the user clicked the slider or handle.
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            handle_x = self._get_handle_x()
            handle_y = self.y + self.height // 2

            bar_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            distance = ((mouse_x - handle_x) ** 2 +
                        (mouse_y - handle_y) ** 2) ** 0.5

            if bar_rect.collidepoint(mouse_x, mouse_y) or distance <= self.handle_radius + 2:
                self.dragging = True
                self._update_from_mouse(mouse_x)

        # Step 12: Stop dragging when the mouse button is released.
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        # Step 13: If dragging, update the value based on mouse position.
        if self.dragging and event.type == pygame.MOUSEMOTION:
            mouse_x, _ = pygame.mouse.get_pos()
            self._update_from_mouse(mouse_x)

    def get_value(self):
        # Step 14: Return the current value.
        return self.value


def drawSatellite(screen, x, y, altitude, radius=10, color=(255, 255, 255)):
    """Draw a simple satellite as a circle on the screen."""
    pygame.draw.circle(screen, color, (int(x), int(y) - int(altitude)), radius)



class OrbitalPhysics:
    def __init__(self, gravitational_constant=0.5):
        """Initializes the physics engine with a universe scale factor (G)."""
        self.G = gravitational_constant

    def calculate_gravity_acceleration(self, body_pos, planet_pos, planet_mass):
        """
        Applies Newton's Law of Universal Gravitation math.
        Returns a Vector2 representing the acceleration pull for this frame.
        """
        # Force the planet position to be a Vector2, even if a tuple was passed in
        planet_vector = pygame.math.Vector2(planet_pos)

        # Then use 'planet_vector' for the rest of the math steps
        direction = planet_vector - body_pos
        # 1. Distance Math: Get the vector pointing from body to planet
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

    def get_orbit_projection(self, ship_pos, ship_vel, planet_pos, planet_mass, steps=250):
        projection_points = []
        status = "stable"  # Default status if nothing bad happens
        
        virtual_pos = pygame.math.Vector2(ship_pos)
        virtual_vel = pygame.math.Vector2(ship_vel)
        
        for _ in range(steps):
            direction = planet_pos - virtual_pos
            distance = direction.length()
            
            # 1. CHECK FOR CRASH
            # If the ship gets within 20 pixels of the planet's center, it hits it.
            if distance < 20: 
                status = "crashed"
                break # Stop calculating further points since it hit the planet
                
            # 2. CHECK FOR ESCAPE (Optional)
            # If it's incredibly far away (e.g., 2000+ pixels), it's leaving orbit.
            if distance > 2000:
                status = "escaped"
                break
            
            # Standard physics steps
            direction_normalized = direction.normalize()
            force_magnitude = (self.G * planet_mass) / (distance ** 2)
            virtual_vel += direction_normalized * force_magnitude
            virtual_pos += virtual_vel
            
            projection_points.append((int(virtual_pos.x), int(virtual_pos.y)))
            
        return projection_points, status
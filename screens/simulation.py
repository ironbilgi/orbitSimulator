import pygame
from classes.sliders import Slider, Dropdown


speed_slider = Slider(40, 140, 260, 20, 0, 100, 50)
altitude_slider = Slider(40, 240, 260, 20, 0, 100, 50)
mass_slider = Slider(40, 360, 260, 20, 1, 1000, 100)
planet_dropdown = Dropdown(
    820, 40, 220, 36, ["Earth", "Mars", "Jupiter", "Moon"])


def simulationScreen(screen, clock, currentScreen, events=None):
    # Fill the background so the scene is visible.
    screen.fill((0, 0, 0))

    # Let the controls respond to the real game events.
    if events is not None:
        for event in events:
            speed_slider.handle_event(event)
            altitude_slider.handle_event(event)
            mass_slider.handle_event(event)
            planet_dropdown.handle_event(event)

    # Pick a base planet color from the dropdown selection.
    selected_planet = planet_dropdown.get_selected()
    planet_colors = {
        "Earth": (0, 255, 0),
        "Mars": (188, 39, 50),
        "Jupiter": (255, 165, 0),
        "Moon": (200, 200, 200),
    }
    planet_color = planet_colors.get(selected_planet, (255, 255, 255))

    # Draw the planet in the middle of the screen.
    pygame.draw.circle(screen, planet_color, (640, 360), 50)

    # Draw the controls on the left side of the screen.
    font = pygame.font.Font(None, 28)

    planet_dropdown.draw(screen, font)
    label = font.render("Base Planet", True, (255, 255, 255))
    label_x = 820 + (220 - label.get_width()) // 2
    screen.blit(label, (label_x, 10))

    speed_label = font.render("Speed", True, (255, 255, 255))
    screen.blit(speed_label, (40, 100))
    speed_slider.draw(screen)
    speed_value = font.render(
        str(int(speed_slider.get_value())), True, (255, 255, 255))
    screen.blit(speed_value, (320, 100))

    altitude_label = font.render("Altitude", True, (255, 255, 255))
    screen.blit(altitude_label, (40, 200))
    altitude_slider.draw(screen)
    altitude_value = font.render(
        str(int(altitude_slider.get_value())), True, (255, 255, 255))
    screen.blit(altitude_value, (320, 200))

    mass_label = font.render("Satellite Mass", True, (255, 255, 255))
    screen.blit(mass_label, (40, 320))
    mass_slider.draw(screen)
    mass_value = font.render(
        str(int(mass_slider.get_value())), True, (255, 255, 255))
    screen.blit(mass_value, (320, 320))

    return currentScreen

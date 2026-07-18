import pygame
from classes.sliders import Slider, Dropdown, drawSatellite
from classes.physics import OrbitalPhysics
from classes.paths import resource_path


speed_slider = Slider(40, 140, 260, 20, 0, 12, 7.5)  # km/s
altitude_slider = Slider(40, 240, 260, 20, 160, 36000, 400)  # km
mass_slider = Slider(40, 360, 260, 20, 1, 1000, 100)

# Real planet masses (kg) are only used for the on-screen "Mass: ..." label.
# The physics engine works in pixel-scale units, so real masses would produce
# wildly disproportionate forces (Earth alone would explode the simulation on
# the first frame). MASS_SCALE converts kg into a small "game mass" that keeps
# accelerations sensible at the altitudes/distances the sim actually uses.
MASS_SCALE = 2e22


def _planet_data(real_mass_kg):
    return {"mass": real_mass_kg, "game_mass": real_mass_kg / MASS_SCALE}


planet_dropdown = Dropdown(
    820, 40, 220, 36, ["Earth", "Mars", "Jupiter", "Moon"],
    data={
        "Earth": _planet_data(5.972e24),
        "Mars": _planet_data(6.417e23),
        "Jupiter": _planet_data(1.898e27),
        "Moon": _planet_data(7.342e22),
    })
button_font = pygame.font.Font(resource_path("assets/fonts/ZenDots-Regular.ttf"), 36)
physics = OrbitalPhysics()


def simulationScreen(screen, clock, currentScreen, events):
    if not hasattr(simulationScreen, "button_scale"):
        simulationScreen.button_scale = 1.0
    if not hasattr(simulationScreen, "gotPressed"):
        simulationScreen.gotPressed = False
        simulationScreen.ship_pos = None
        simulationScreen.ship_vel = None
    # Fill the background so the scene is visible.
    screen.fill((0, 0, 0))

    # Let the controls respond to the real game events.
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

    # Draw a back button in the top-left corner to return to the home screen.
    back_text = font.render("< Back", True, (255, 255, 255))
    back_rect = pygame.Rect(20, 20, back_text.get_width() + 20, back_text.get_height() + 16)
    back_hovered = back_rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(screen, (44, 255, 5) if back_hovered else (150, 150, 150), back_rect, 2)
    screen.blit(back_text, (back_rect.x + 10, back_rect.y + 8))

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back_hovered:
            # Reset the sim state so re-entering this screen later starts fresh.
            simulationScreen.gotPressed = False
            simulationScreen.ship_pos = None
            simulationScreen.ship_vel = None
            return "HOME"

    # Draw the dropdown menu for selecting the base planet.
    planet_dropdown.draw(screen, font)
    label = font.render("Base Planet", True, (255, 255, 255))
    label_x = 820 + (220 - label.get_width()) // 2
    screen.blit(label, (label_x, 10))
    
    # Display the mass of the selected planet below the dropdown once a choice has been made.
    if not planet_dropdown.open and planet_dropdown.has_selection():
        mass = planet_dropdown.get_data("mass")
        if mass:
            mass_text = font.render(f"Mass: {mass:.2e} kg", True, (200, 200, 200))
            screen.blit(mass_text, (820, 90))

    # Draw the sliders and their labels on the left side of the screen.
    speed_label = font.render("Speed", True, (255, 255, 255))
    screen.blit(speed_label, (40, 100))
    speed_slider.draw(screen)
    speed_value = font.render(
        str(int(speed_slider.get_value())), True, (255, 255, 255))
    screen.blit(speed_value, (320, 100))

    # Draw the altitude slider and its label on the left side of the screen.
    altitude_label = font.render("Altitude", True, (255, 255, 255))
    screen.blit(altitude_label, (40, 200))
    altitude_slider.draw(screen)
    altitude_value = font.render(
        str(int(altitude_slider.get_value())), True, (255, 255, 255))
    screen.blit(altitude_value, (320, 200))


    # Draw the mass slider and its label on the left side of the screen.
    mass_label = font.render("Satellite Mass", True, (255, 255, 255))
    screen.blit(mass_label, (40, 320))
    mass_slider.draw(screen)
    mass_value = font.render(
        str(int(mass_slider.get_value())), True, (255, 255, 255))
    screen.blit(mass_value, (320, 320))

    #Draw the satellite based on the altitude slider value, ensuring it stays within a reasonable range.
    visual_altitude = max(50, min(300, (altitude_slider.get_value() - 160) / 35840 * 250 + 50))
    drawSatellite(screen, 640, 360, visual_altitude, radius=10, color=(255, 255, 255))

    # Draws the simulate button on the bottom center of the screen.
    #Bad code repetitive, but its whatever for a final project/prototype
    simulate_button = button_font.render("Simulate", True, (44, 255, 5))
    button_rect = pygame.Rect(0, 0, simulate_button.get_width() + 20, simulate_button.get_height() + 20)
    button_rect.center = (screen.get_width() // 2, 600)
    hovered = button_rect.collidepoint(pygame.mouse.get_pos())

    target_scale = 1.12 if hovered else 1.0
    simulationScreen.button_scale += (target_scale - simulationScreen.button_scale) * 0.2

    scaled_simulate_button = pygame.transform.scale_by(simulate_button, simulationScreen.button_scale)
    scaled_rect = pygame.Rect(0, 0, scaled_simulate_button.get_width() + 20, scaled_simulate_button.get_height() + 20)
    scaled_rect.center = (screen.get_width() // 2, 600)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    hovered = scaled_rect.collidepoint(mouse_x, mouse_y)

    screen.blit(scaled_simulate_button, (scaled_rect.x + 10, scaled_rect.y + 10))
    pygame.draw.rect(screen, (44, 255, 5), scaled_rect, 2)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hovered:
            simulationScreen.gotPressed = not simulationScreen.gotPressed  # Toggle state on/off
            if simulationScreen.gotPressed:
                # Place ship directly above the planet using the slider value
                simulationScreen.ship_pos = pygame.math.Vector2(640, 360 - visual_altitude)
                # Give it a sideways velocity based on the speed slider
                simulationScreen.ship_vel = pygame.math.Vector2(speed_slider.get_value(), 0)
            break

    # Run physics loop continuously while toggled on
    if simulationScreen.gotPressed and simulationScreen.ship_pos and planet_dropdown.has_selection():
        p_mass = planet_dropdown.get_data("game_mass")

        # 1. Update position
        simulationScreen.ship_pos, simulationScreen.ship_vel = physics.update_body(
            simulationScreen.ship_pos, simulationScreen.ship_vel, pygame.math.Vector2(640, 360), p_mass)

        # 2. Project future orbit path
        orbit_line, currentStatus = physics.get_orbit_projection(
            simulationScreen.ship_pos, simulationScreen.ship_vel, pygame.math.Vector2(640, 360), p_mass, steps=250)

        # 3. Draw the trajectory projection path line
        if len(orbit_line) > 1:
            pygame.draw.lines(screen, (0, 150, 255), False, orbit_line, 1)

        # 4. Check conditions (Notice we DO NOT clear gotPressed here so it keeps running!)
        if currentStatus == "crashed":
            print("The satellite has crashed into the planet.")
            simulationScreen.gotPressed = False # Turn off engine only when simulation ends
        elif currentStatus == "escaped":
            print("The satellite has escaped the planet's gravity.")
            simulationScreen.gotPressed = False

        # Draw the active, moving satellite
        pos = simulationScreen.ship_pos
        pygame.draw.circle(screen, (255, 255, 255), (int(pos.x), int(pos.y)), 10)
    else:
        # If the simulation hasn't started yet, just draw the static preview satellite
        drawSatellite(screen, 640, 360, visual_altitude, radius=10, color=(255, 255, 255))

    return currentScreen
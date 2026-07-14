import random

import pygame
import math
import colorsys
from planets import Planet

pygame.init()


# create font once to avoid recreating every frame
font = pygame.font.Font("assets/fonts/ZenDots-Regular.ttf", 80)

# create the planet once so its orbit state persists across frames
mecury = Planet("Mercury", 3.285e23, 10,
                (169, 169, 169), 60, 1.2, 0, False, True)
venus = Planet("Venus", 4.867e24, 15, (255, 165, 0), 80, 0.8, 0, False, True)
earth = Planet("Earth", 5.972e24, 20, (78, 128, 62), 100, 0.5, 0, False, True)
moon = Planet("Moon", 7.348e22, 5, (200, 200, 200), 30, 1.0, 0, False, True)
mars = Planet("Mars", 6.39e23, 15, (188, 39, 50), 150, 0.3, 0, False, True)
jupiter = Planet("Jupiter", 1.898e27, 30, (255, 165, 0),
                 200, 0.2, 0, False, True)
saturn = Planet("Saturn", 5.683e26, 25, (210, 180, 140),
                250, 0.15, 0, False, True)
uranus = Planet("Uranus", 8.681e25, 20, (173, 216, 230),
                300, 0.1, 0, False, True)
neptune = Planet("Neptune", 1.024e26, 20, (0, 0, 255),
                 350, 0.08, 0, False, True)


def homeScreen(screen, clock):
    # draw the home screen
    screen.fill((20, 20, 30))

    # Create floating animation using sine wave
    time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
    bob = math.sin(time * 2) * 15  # Bobs up and down 15 pixels

    # Slow rainbow color by cycling the HSV hue over time
    hue = (time * 0.08) % 1.0  # full cycle ~12.5s
    r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 1.0)
    color = (int(r * 255), int(g * 255), int(b * 255))

    title = font.render("Orbit Simulator", True, color)
    playButton = font.render("Play", True, (44, 255, 5))

    #Random Stars

    pygame.draw.circle(screen, (255, 255, 255), (random.randint(0, screen.get_width()), random.randint(0, screen.get_height())), 1)
    # Draw the solar system first so the UI can appear on top when they overlap
    pygame.draw.circle(screen, (180, 150, 80), (screen.get_width(
    ) / 2, screen.get_height() / 2), 40)  # Sun

    # Update and draw planets, Mercury
    mecury.update_position(clock.get_time() / 1000.0)
    mecury.draw(screen, screen.get_width() / 2, screen.get_height() / 2)

    # Venus
    venus.update_position(clock.get_time() / 1000.0)
    venus.draw(screen, screen.get_width() / 2, screen.get_height() / 2)

    # Earth
    earth.update_position(clock.get_time() / 1000.0)
    earth.draw(screen, screen.get_width() / 2, screen.get_height() / 2)

    # Moon
    moon.update_position(clock.get_time() / 1000.0)
    moon.draw(screen, *earth.get_position(screen.get_width() /
              2, screen.get_height() / 2))

    # Mars
    mars.update_position(clock.get_time() / 1000.0)
    mars.draw(screen, screen.get_width() / 2, screen.get_height() / 2)

    # Jupiter
    jupiter.update_position(clock.get_time() / 1000.0)
    jupiter.draw(screen, screen.get_width() / 2, screen.get_height() / 2)

    # Saturn
    saturn.update_position(clock.get_time() / 1000.0)
    saturn.draw(screen, screen.get_width() / 2, screen.get_height() / 2)

    # Uranus
    uranus.update_position(clock.get_time() / 1000.0)
    uranus.draw(screen, screen.get_width() / 2, screen.get_height() / 2)

    # Neptune
    neptune.update_position(clock.get_time() / 1000.0)
    neptune.draw(screen, screen.get_width() / 2, screen.get_height() / 2)

    # Draw the UI text and button last so they appear on top
    screen.blit(title, (screen.get_width() / 2 -
                title.get_width() / 2, 100 + bob))
    screen.blit(playButton, (screen.get_width() /
                2 - playButton.get_width() / 2, 500))
    pygame.draw.rect(screen, (44, 255, 5), (screen.get_width() / 2 - playButton.get_width() /
                     2 - 10, 500 - 10, playButton.get_width() + 20, playButton.get_height() + 20), 3)


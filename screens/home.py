import pygame
import math
import colorsys
from planets import Planet

pygame.init()


# create font once to avoid recreating every frame
font = pygame.font.Font("assets/fonts/ZenDots-Regular.ttf", 80)

# create the planet once so its orbit state persists across frames
earth = Planet("Earth", 5.972e24, 20, (78, 128, 62), 100, 0.5, 0)
moon = Planet("Moon", 7.348e22, 5, (200, 200, 200), 30, 1.0, 0)


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
    screen.blit(title, (screen.get_width() / 2 - title.get_width() / 2, 100 + bob))

    playButton = font.render("Play", True, (44, 255, 5))
    screen.blit(playButton, (screen.get_width() / 2 - playButton.get_width() / 2, 500))
    pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() / 2 - playButton.get_width() /  2 - 10, 500 - 10, playButton.get_width() + 20, playButton.get_height() + 20), 3)

    # creating solar system

    pygame.draw.circle(screen, (255, 255, 0), (screen.get_width() / 2 - 100, screen.get_height() / 2), 40)  # Sun

    earth.update_position(clock.get_time() / 1000.0)
    earth.draw(screen, screen.get_width() / 2 - 100, screen.get_height() / 2)
    moon.update_position(clock.get_time() / 1000.0)
    moon.draw(screen, *earth.get_position(screen.get_width() / 2 - 100, screen.get_height() / 2))




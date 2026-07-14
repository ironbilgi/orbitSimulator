import pygame
import math
import colorsys

pygame.init()


# create font once to avoid recreating every frame
font = pygame.font.Font("assets/fonts/ZenDots-Regular.ttf", 80)


def homeScreen(screen):
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
    # draw only the border of the button (width=3) and use integer rect
    btn_x = int(screen.get_width() / 2 - playButton.get_width() / 2 - 20)
    btn_y = 320
    btn_w = playButton.get_width() + 40
    btn_h = playButton.get_height() + 20
    pygame.draw.rect(screen, (255, 255, 255), (btn_x, btn_y, btn_w, btn_h), 3)
    screen.blit(playButton, (screen.get_width() / 2 - playButton.get_width() / 2, 330))

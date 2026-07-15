import pygame
import math


def simulationScreen(screen, clock, currentScreen):
    # Placeholder for the simulation screen
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Simulation Screen", True, (255, 255, 255))
    screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2,
                       screen.get_height() / 2 - text.get_height() / 2))

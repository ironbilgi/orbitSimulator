import pygame
from screens.home import homeScreen
# initialize pygame
pygame.init()
# initialize the screen
screen = pygame.display.set_mode((1280, 720))
# The top bar of the window will say "Orbit Simulator"
pygame.display.set_caption("Orbit Simulator")
# nickname for true
running = True
# creates the clock object
clock = pygame.time.Clock()
currentScreen = "HOME"

currentTrack = pygame.mixer.Sound(
    "assets/soundTracks/audiopapkin-ambient-soundscapes-001-space-atmosphere-303246.mp3")
currentTrack.set_volume(0.1)
currentTrack.play(-1)  # Loop indefinitely
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if currentScreen == "HOME":
        homeScreen(screen, clock)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame

# Initialize all imported pygame modules
pygame.init()

# Create a display window
screen = pygame.display.set_mode((800, 600))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
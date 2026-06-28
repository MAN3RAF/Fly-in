# from zone import Zone
# from connection import Connection
# from graph import Graph
# from drone import Drone
import pygame


pygame.init()


screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

running = True

bread_image = pygame.image.load("src/cs.png")

clock = pygame.time.Clock()

x = 0
y = 30

while running:

	screen.blit(bread_image, (x, y)) 


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
	x += 1

	clock.tick(20)
	
	pygame.display.flip()

pygame.quit()



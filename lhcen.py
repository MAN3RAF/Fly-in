import pygame



pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("LHCEN Simulation")


running = True
lon = (0, 0, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_q:
                lon = (255, 0, 0)

    screen.fill(lon)
    image = pygame.font.Font(None, 36).render("Hello!", True, (255, 255, 255))
    screen.blit(image, (10, 20))

    pygame.draw.circle(screen, (10, 89, 90), (screen.get_width() // 2, screen.get_height()//2), 100, width=3)

    pygame.display.flip()


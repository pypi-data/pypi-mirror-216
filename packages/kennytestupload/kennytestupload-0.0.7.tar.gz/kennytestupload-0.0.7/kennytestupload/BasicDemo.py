import pygame

#Game Setup
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Demo')
clock = pygame.time.Clock()
# test_font = pygame.font.Font('font/XXXXX.ttf', 50)
game_active = True

#Load immage as surface
player_surface = pygame.image.load('data/alien3.png').convert_alpha()

#Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active:
        screen.blit(player_surface, (400, 200))

    pygame.display.update()
    clock.tick(60)

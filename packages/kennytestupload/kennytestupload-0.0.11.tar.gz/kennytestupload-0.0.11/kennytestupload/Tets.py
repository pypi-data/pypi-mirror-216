import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_surface = pygame.image.load('data/enemy2.png').convert_alpha();
        player_surface = pygame.transform.scale(player_surface, (64, 64))
        self.image = player_surface
        self.rect = self.image.get_rect(center=(250, 250))
        self.speed = 2

    def player_input_move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def update(self):
        self.player_input_move()

#Init
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Demo")
clock = pygame.time.Clock()
game_active = True

player_group = pygame.sprite.GroupSingle()
player_group.add(Player())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((0, 0, 0))

    if game_active:
        player_group.draw(screen)
        player_group.update()

    pygame.display.update()

#Homework:
'''
Find all the images and backgrounds you want to create
For example:
-Player
-Enemies
-Platform
-Ground
-Background
-Dead effect (explosion? Blood spill?, flashes?)
-Sounds effects (shooting?, jumping?, enemy growling?)

Code:
- Create classes and have each load their corresponding sprite
- Draw the onto the screen. 
'''
import pygame

#Game Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Demo')
clock = pygame.time.Clock()
# test_font = pygame.font.Font('font/XXXXX.ttf', 50)
game_active = True

#Player Class
class Player(pygame.sprite.Sprite):

    def __init__(self, startLocation):
        super().__init__()
        player_image_frame1 = pygame.image.load('data/alien3.png').convert_alpha()
        player_image_frames = [player_image_frame1]
        self.image = player_image_frames[0]
        self.rect = self.image.get_rect(center = startLocation)
        self.speed = 4

    def player_input(self):
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
        self.player_input()


#Setup game
sky = pygame.image.load('data/sky.png').convert()
ground = pygame.image.load('data/ground.png').convert()


player = pygame.sprite.GroupSingle()
player.add(Player(startLocation=(80, 200)))

player2 = pygame.sprite.GroupSingle() #Simulate groups of enemies
player2.add(Player(startLocation=(250, 200)))


#Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #Draw background that exists in all mopde
    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, 300))

    if game_active:
        player.draw(screen)
        player.update()
        player2.draw(screen)

        #detect collision

        if len(player2) > 0:
            if player.sprite.rect.colliderect(player2.sprite.rect):
                player2.sprite.kill()



    pygame.display.update()
    clock.tick(60)

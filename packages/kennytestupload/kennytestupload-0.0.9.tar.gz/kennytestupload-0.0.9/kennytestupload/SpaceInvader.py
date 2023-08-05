import pygame
import os

#Setup game
def Main():
    # Game Setup
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption('Demo')
    clock = pygame.time.Clock()
    time_elapsed_since_start = 0
    delta_time = 0
    # test_font = pygame.font.Font('font/XXXXX.ttf', 50)
    game_active = True

    # Player Class
    class Player(pygame.sprite.Sprite):

        def __init__(self, startLocation):
            super().__init__()
            player_image_frame1 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'data/alien3.png')).convert_alpha()
            player_image_frames = [player_image_frame1]
            self.image = player_image_frames[0]
            self.rect = self.image.get_rect(center=startLocation)
            self.speed = 4

        def player_input(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            # if keys[pygame.K_UP]:
            #     self.rect.y -= self.speed
            # if keys[pygame.K_DOWN]:
            #     self.rect.y += self.speed

        def update(self):
            self.player_input()

    # Player Class
    class Enemy(pygame.sprite.Sprite):

        def __init__(self, startLocation):
            super().__init__()
            enemy_image_frame1 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'data/enemy2.png')).convert_alpha()
            enemy_image_frame1 = pygame.transform.scale(enemy_image_frame1, (50, 50))
            player_image_frames = [enemy_image_frame1]
            self.image = player_image_frames[0]
            self.rect = self.image.get_rect(center=startLocation)
            self.speed = 1
            self.direction = 1
            self.move_timer = 0
            self.move_threshold = 30

        def move(self):
            self.move_timer += delta_time
            if self.direction == 1:
                if self.move_timer > self.move_threshold:
                    self.rect.x -= self.speed
                    self.move_timer = 0
            # if keys[pygame.K_UP]:
            #     self.rect.y -= self.speed
            # if keys[pygame.K_DOWN]:
            #     self.rect.y += self.speed

        def update(self):
            self.move()


    player = pygame.sprite.GroupSingle()
    player.add(Player(startLocation=(300, 450)))

    enemies = pygame.sprite.Group()
    for i in range(50, 151, 50):
        for j in range(80, 520, 60):
            enemies.add(Enemy(startLocation=(j, i)))

    #Main game loop
    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if game_active:
            player.draw(screen)
            player.update()
            enemies.draw((screen))
            enemies.update()


        pygame.display.update()
        delta_time = clock.tick()
        time_elapsed_since_start += delta_time

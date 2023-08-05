import pygame
import os

def Main():
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            player_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), 'player.jpg')).convert_alpha()
            player_surface = pygame.transform.scale(player_surface, (64, 64))
            self.image = player_surface
            self.rect = self.image.get_rect(center=(250, 250))
            self.speed = 4
            self.gravity_original = 1
            self.gravity = 1
            self.speedY = 0
            self.max_drop_speed = 5
            self.on_ground = False
            self.jump_force = 15

        def player_input_move(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_UP]:
                if self.on_ground:
                    self.on_ground = False
                    self.speedY -= self.jump_force
                    self.gravity = self.gravity_original
            # if keys[pygame.K_DOWN]:
            #     self.rect.y += self.speed

        def detect_out_of_screen(self):
            if self.rect.top > screen_height:
                return True
            return False

        def detect_enemy(self, object):
            if self.rect.colliderect(object):
                return True
            return False

        def detect_ground(self, object):
            if self.rect.colliderect(object) and object.rect.top - self.rect.bottom > -5:
                    self.on_ground = True
                    self.speedY = 0
                    self.gravity = 0
            else:
                self.on_ground = False
                self.gravity = self.gravity_original

        def update_speedY(self):
            if self.speedY < self.max_drop_speed:
                self.speedY += self.gravity 

        def move(self):
            self.rect.y += self.speedY

        def update(self):
            self.player_input_move()
            self.update_speedY()
            self.move()
            self.detect_out_of_screen()


    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            enemy_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), 'enemy1.jpg')).convert_alpha()
            enemy_surface = pygame.transform.scale(enemy_surface, (64, 64))
            self.image = enemy_surface
            self.rect = self.image.get_rect(center=(100, 250))

    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            platform_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), 'platform1.jpg')).convert_alpha()
            platform_surface = pygame.transform.scale(platform_surface, (64, 64))
            self.image = platform_surface
            self.rect = self.image.get_rect(center=(x, y))

    class Level1():
        def __init__(self):
            self.platform_group = pygame.sprite.Group()
            self.platform_group.add(Platform(250, 400))
            self.platform_group.add(Platform(400, 400))

        def draw(self, screen):
            self.platform_group.draw(screen)

    #Init
    pygame.init()
    screen_width = 500
    screen_height = 500
    game_mode = 0 #0 = start screen  1 = game_running  2 = death_screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Demo")
    clock = pygame.time.Clock()

    #Sprite setups 
    bg_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), 'background.jpg')).convert()

    player_group = pygame.sprite.GroupSingle()
    player_group.add(Player())

    enemy_group = pygame.sprite.GroupSingle()
    enemy_group.add(Enemy())

    level1 = Level1()
    # platform_group = pygame.sprite.GroupSingle()
    # platform_group.add(Platform())

    dt = 0


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))

        if game_mode == 0:
            screen.blit(bg_surface, (0, 0))
            #Run text optionally
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_mode = 1

        if game_mode == 1:
            dt = clock.tick(30)
            player_group.draw(screen)
            player_group.update()
            enemy_group.draw(screen)
            # platform_group.draw(screen)
            # for platform in level1.platform_group.sprites():
            #     platform
            # level1.platform_group.draw(screen)
            level1.draw(screen)
            # print(level1.platform_group)
            for platform in level1.platform_group.sprites(): #Debug this 
                player_group.sprite.detect_ground(platform)
            if player_group.sprite.detect_enemy(enemy_group.sprite):
                game_mode = 0
            if player_group.sprite.detect_out_of_screen():
                game_mode = 0
            

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
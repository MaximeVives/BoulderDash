import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('sprites/player.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.move_ticker = 0
        self.speed = 16
        self.images = {
            'down': self.get_image(0, 64),
            'left': self.get_image(0, 16),
            'right': self.get_image(0, 48),
            'up': self.get_image(0, 0),
        }
        self.feet = pygame.Rect(0, 0, 16, 16)
        self.old_position = self.position.copy()

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey([0, 0, 0])

    def change_speed(self, is_Faster):
        if is_Faster:
            if self.speed == 2:
                self.speed += 1
        else:
            self.speed = 2

    def move(self, key):
        axe = 0
        orientation = 0

        if self.move_ticker == 0:
            if key not in ['z', 'q', 's', 'd']:
                pass
            elif key in ['z', 's']:
                axe = 1
                orientation = -1 if key == 'z' else 1
            elif key in ['q', 'd']:
                axe = 0
                orientation = 1 if key == 'd' else -1
            self.move_ticker = 10
        else:
            self.move_ticker -= 1

        print(self.position)
        self.position[axe] += orientation * self.speed * 8

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.update()

    def get_image(self, x, y):
        image = pygame.Surface([16, 16])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 16))
        return image

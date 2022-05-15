import pygame
import pytmx
import pyscroll

from player import Player


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Boulder Bled")

        # Initialisation
        self.tmx_data = None
        self.map_data = None
        self.map_layer = None
        self.walls = None
        self.group = None
        self.enter_house_rect = None

        # Charger la carte
        self.load_map("Map/map.tmx")

        # Générer un player
        print(self.tmx_data)
        player_position = self.tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # Rectangles de collisions
        self.load_collision()

        # Dessiner le groupe de calque
        self.load_calques()

        self.map = "world"

    def reinitialisation(self):
        self.tmx_data = None
        self.map_data = None
        self.map_layer = None
        self.walls = None
        self.group = None
        self.enter_house_rect = None

    def load_map(self, file):
        self.tmx_data = pytmx.util_pygame.load_pygame(file)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 1.7

    def load_collision(self):
        self.walls = [
            pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            for obj in self.tmx_data.objects
            if obj.type == "Collision"
        ]

    def load_calques(self):
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
        self.group.add(self.player)

    # def load_rect_exit(self, rect_coll_name):
    #     enter_house = self.tmx_data.get_object_by_name(rect_coll_name)
    #     self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    def load_spawn(self, spawn_name):
        spawn = self.tmx_data.get_object_by_name(spawn_name)
        self.player.position[0] = spawn.x
        self.player.position[1] = spawn.y

        self.player.save_location()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LSHIFT]:
            self.player.change_speed(is_Faster=True)
        else:
            self.player.change_speed(is_Faster=False)

        if pressed[pygame.K_z]:
            self.player.move("z")
            self.player.change_animation("up")

        if pressed[pygame.K_s]:
            self.player.move("s")
            self.player.change_animation("down")

        if pressed[pygame.K_d]:
            self.player.move("d")
            self.player.change_animation("right")

        if pressed[pygame.K_q]:
            self.player.move("q")
            self.player.change_animation("left")

    def update(self):
        self.group.update()

        for spte in self.group.sprites():
            if spte.feet.collidelist(self.walls) > -1:
                spte.move_back()

    def run(self):
        clock = pygame.time.Clock()

        # Boucle du jeu
        running = True

        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()

import os
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Board:
    def __init__(self, group):
        for i in range(400):
            if i == 0:
                image = load_image("Slice 122.png")
            elif 0 < i < 19:
                image = load_image("Slice 124.png")
            elif i == 19:
                image = load_image("Slice 126.png")
            elif i == 120:
                image = load_image("Slice 128.png")
            elif i == 380:
                image = load_image("Slice 142.png")
            elif i == 399:
                image = load_image("Slice 146.png")
            elif i % 10 == 9 and (i + 1) / 10 % 2 == 0 and 150 < i < 400:
                image = load_image("Slice 136.png")
            elif i / 10 % 2 == 0 and 120 < i < 400:
                image = load_image("Slice 132.png")
            elif i / 10 % 2 == 0:
                image = load_image("Slice 133.png")
            elif i == 139:
                image = load_image("Slice 130.png")
            elif i % 10 == 9 and (i + 1) / 10 % 2 == 0 and 20 < i < 140:
                image = load_image("Slice 135.png")
            elif i % 10 != 0 and 20 < i < 120:
                image = load_image("Slice 129.png")
            elif i % 10 != 0 and 120 < i < 140 and i != 130:
                image = load_image("Slice 134.png")
            elif 380 < i < 399:
                image = load_image("Slice 144.png")
            elif i % 10 != 0 and 140 < i < 400:
                image = load_image("Slice 1.png")
            # Расположение по x;
            # (i // 10) столбец; * 24 расстояние между спрайтами в 24 пикселя (ширина одного спрайта); + 24 отступ
            x = (i % 20) * 24 + 24
            # Расположение по y;
            # (i // 10) строка; * 24 расстояние между спрайтами в 24 пикселя (ширина одного спрайта); + 24 отступ
            y = (i // 20) * 24 + 24
            # создание и добавление спрайта в группу
            sprite = pygame.sprite.Sprite()
            sprite.image = image
            sprite.rect = sprite.image.get_rect(topleft=(x, y))
            group.add(sprite)
        # Дверь
        self.door_sprite = pygame.sprite.Sprite()
        image = load_image('door.png')
        self.door_sprite.image = image
        self.door_sprite.rect = self.door_sprite.image.get_rect(topleft=(256, 100))
        group.add(self.door_sprite)

    def get_door_sprite(self):
        return self.door_sprite


class Creature(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("Idle Front.png")
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 205

    def update(self, *args):
        if args:
            if 30 < self.rect.x + args[0][0] < 436:
                self.rect.x += args[0][0]
            if 135 < self.rect.y + args[0][1] < 425:
                self.rect.y += args[0][1]

    def check_interaction_door(self, door_sprite):
        # Проверяем, находится ли игрок рядом с дверью
        if self.rect.colliderect(door_sprite.rect):
            return True
        return False


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Organs')
    size = width, height = 524, 524
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    board = Board(all_sprites)
    creature = Creature(all_sprites)
    FPS = 30
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        screen.fill('black')
        if keys[pygame.K_a]:
            all_sprites.update((-10, 0))
        elif keys[pygame.K_d]:
            all_sprites.update((10, 0))
        elif keys[pygame.K_w]:
            all_sprites.update((0, -10))
        elif keys[pygame.K_s]:
            all_sprites.update((0, 10))
        if keys[pygame.K_e]:
            if creature.check_interaction_door(board.get_door_sprite()):
                print("взаимодействует с дверью")

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()

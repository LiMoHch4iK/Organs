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


class Bedroom:
    def __init__(self, group):
        for i in range(400):
            if i == 0:  # левый верхний угол обоев (задняя стена)
                image = load_image("Slice 122.png")
            elif 0 < i < 19:  # верхний край стены (задняя стена)
                image = load_image("Slice 124.png")
            elif i == 19:  # правый верхний угол обоев (задняя стена)
                image = load_image("Slice 126.png")
            elif i == 120:  # правый нижний угол обоев (задняя стена)
                image = load_image("Slice 128.png")
            elif i == 380:  # левый нижний угол обоев (передняя стена)
                image = load_image("Slice 142.png")
            elif i == 399:  # правый нижний угол обоев (передняя стена)
                image = load_image("Slice 146.png")
            elif i == 139:  # правый нижний угол обоев (задняя стена)
                image = load_image("Slice 130.png")
            elif i % 10 == 9 and (i + 1) / 10 % 2 == 0 and 150 < i < 400:  # правая стена рядом с полом
                image = load_image("Slice 136.png")
            elif i / 10 % 2 == 0 and 120 < i < 400:  # левая стена рядом с полом
                image = load_image("Slice 132.png")
            elif i / 10 % 2 == 0:  # левая стена рядом со стеной
                image = load_image("Slice 133.png")
            elif i % 10 == 9 and (i + 1) / 10 % 2 == 0 and 20 < i < 140:  # правая стена рядом со стеной
                image = load_image("Slice 135.png")
            elif i % 10 != 0 and 20 < i < 120:  # общий тон задней стены
                image = load_image("Slice 129.png")
            elif i % 10 != 0 and 120 < i < 140 and i != 130:  # нижний край стены (задняя стена)
                image = load_image("Slice 134.png")
            elif 380 < i < 399:  # нижний край стены (передняя стена)
                image = load_image("Slice 144.png")
            elif i % 10 != 0 and 140 < i < 400:  # пол
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
        self.door1_sprite = pygame.sprite.Sprite()
        image = load_image('door.png')
        self.door1_sprite.image = image
        self.door1_sprite.rect = self.door1_sprite.image.get_rect(topleft=(200, 100))
        group.add(self.door1_sprite)

    def get_door_sprite(self):
        return self.door1_sprite


class LivingRoom:
    def __init__(self, group):
        for i in range(400):
            if i == 0:  # левый верхний угол обоев (задняя стена)
                image = load_image("Slice 61.png")
            elif 0 < i < 19:  # верхний край стены (задняя стена)
                image = load_image("Slice 63.png")
            elif i == 19:  # правый верхний угол обоев (задняя стена)
                image = load_image("Slice 65.png")
            elif i == 120:  # правый нижний угол обоев (задняя стена)
                image = load_image("Slice 67.png")
            elif i == 380:  # левый нижний угол обоев (передняя стена)
                image = load_image("Slice 81.png")
            elif i == 399:  # правый нижний угол обоев (передняя стена)
                image = load_image("Slice 85.png")
            elif i == 139:  # правый нижний угол обоев (задняя стена)
                image = load_image("Slice 69.png")
            elif i % 10 == 9 and (i + 1) / 10 % 2 == 0 and 150 < i < 400:  # правая стена рядом с полом
                image = load_image("Slice 75.png")
            elif i / 10 % 2 == 0 and 120 < i < 400:  # левая стена рядом с полом
                image = load_image("Slice 71.png")
            elif i / 10 % 2 == 0:  # левая стена рядом со стеной
                image = load_image("Slice 72.png")
            elif i % 10 == 9 and (i + 1) / 10 % 2 == 0 and 20 < i < 140:  # правая стена рядом со стеной
                image = load_image("Slice 74.png")
            elif i % 10 != 0 and 20 < i < 120:  # общий тон задней стены
                image = load_image("Slice 68.png")
            elif i % 10 != 0 and 120 < i < 140 and i != 130:  # нижний край стены (задняя стена)
                image = load_image("Slice 73.png")
            elif i == 386:  # левый угол передней стены у двери
                image = load_image("Slice 82.png")
            elif 380 < i < 387 or 389 < i < 399:  # нижний край стены (передняя стена)
                image = load_image("Slice 83.png")
            elif i == 389:  # правый угол передней стены у двери
                image = load_image("Slice 84.png")
            elif i % 10 != 0 and 140 < i < 400:  # пол
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
        # Прошлая дверь
        self.door_sprite1 = pygame.sprite.Sprite()
        image = load_image('Slice 4.png')
        self.door_sprite1.image = image
        self.door_sprite1.rect = self.door_sprite1.image.get_rect(topleft=(192, 480))
        group.add(self.door_sprite1)
        self.door_sprite1 = pygame.sprite.Sprite()
        image = load_image('Slice 4.png')
        self.door_sprite1.image = image
        self.door_sprite1.rect = self.door_sprite1.image.get_rect(topleft=(216, 480))
        group.add(self.door_sprite1)
        # Новая дверь
        self.door_sprite2 = pygame.sprite.Sprite()
        image = load_image('door.png')
        self.door_sprite2.image = image
        self.door_sprite2.rect = self.door_sprite2.image.get_rect(topleft=(256, 100))
        group.add(self.door_sprite2)

    def get_door_sprite(self):
        return self.door_sprite1

    def get_door_sprite2(self):
        return self.door_sprite2


class Corridor:
    def __init__(self, group):
        for i in range(200):
            if i == 0:  # левый верхний угол обоев (задняя стена)
                image = load_image("Slice 61.png")
            elif 0 < i < 9:  # верхний край стены (задняя стена)
                image = load_image("Slice 63.png")
            elif i == 9:  # правый верхний угол обоев (задняя стена)
                image = load_image("Slice 65.png")
            elif i == 60:  # правый нижний угол обоев (задняя стена)
                image = load_image("Slice 67.png")
            elif i == 190:  # левый нижний угол обоев (передняя стена)
                image = load_image("Slice 81.png")
            elif i == 199:  # правый нижний угол обоев (передняя стена)
                image = load_image("Slice 85.png")
            elif i == 69:  # правый нижний угол обоев (задняя стена)
                image = load_image("Slice 69.png")
            elif i % 10 == 0 and 9 < i < 70:  # левая стена рядом со стеной
                image = load_image("Slice 72.png")
            elif i % 10 == 9 and 10 < i < 70:  # правая стена рядом со стеной
                image = load_image("Slice 74.png")
            elif i % 10 != 0 and 60 < i < 70:  # нижний край стены (задняя стена)
                image = load_image("Slice 73.png")
            elif i % 10 != 0 and 10 < i < 70:  # общий тон задней стены
                image = load_image("Slice 68.png")
            elif i % 10 == 9 and 75 < i < 200:  # правая стена рядом с полом
                image = load_image("Slice 75.png")
            elif i % 10 == 0 and 59 < i < 200:  # левая стена рядом с полом
                image = load_image("Slice 71.png")
            elif i == 193:  # левый угол передней стены у двери
                image = load_image("Slice 82.png")
            elif 190 < i < 193 or 196 < i < 299:  # нижний край стены (передняя стена)
                image = load_image("Slice 83.png")
            elif i == 196:  # правый угол передней стены у двери
                image = load_image("Slice 84.png")
            elif i % 10 != 0 and 70 < i < 400:  # пол
                image = load_image("Slice 1.png")
            # Расположение по x;
            # (i // 10) столбец; * 24 расстояние между спрайтами в 24 пикселя (ширина одного спрайта); + 24 отступ
            x = (i % 10) * 24 + 142
            # Расположение по y;
            # (i // 10) строка; * 24 расстояние между спрайтами в 24 пикселя (ширина одного спрайта); + 24 отступ
            y = (i // 10) * 24 + 24
            # создание и добавление спрайта в группу
            sprite = pygame.sprite.Sprite()
            sprite.image = image
            sprite.rect = sprite.image.get_rect(topleft=(x, y))
            group.add(sprite)
        # Прошлая дверь
        self.door_sprite2 = pygame.sprite.Sprite()
        image = load_image('Slice 4.png')
        self.door_sprite2.image = image
        self.door_sprite2.rect = self.door_sprite2.image.get_rect(topleft=(238, 480))
        group.add(self.door_sprite2)
        self.door_sprite2 = pygame.sprite.Sprite()
        image = load_image('Slice 4.png')
        self.door_sprite2.image = image
        self.door_sprite2.rect = self.door_sprite2.image.get_rect(topleft=(262, 480))
        group.add(self.door_sprite2)
        # Новая дверь
        self.door_sprite3 = pygame.sprite.Sprite()
        image = load_image('door.png')
        self.door_sprite3.image = image
        self.door_sprite3.rect = self.door_sprite3.image.get_rect(topleft=(238, 100))
        group.add(self.door_sprite3)

    def get_door_sprite2(self):
        return self.door_sprite2

    def get_door_sprite3(self):
        return self.door_sprite3


class Kitchen:
    def __init__(self, group):
        for i in range(400):
            if i == 0:  # левый верхний угол обоев (задняя стена)
                image = load_image("Slice 61.png")
            elif 0 < i < 19:  # верхний край стены (задняя стена)
                image = load_image("Slice 63.png")
            elif i == 19:  # правый верхний угол обоев (задняя стена)
                image = load_image("Slice 65.png")
            elif i == 120:  # правый нижний угол обоев (задняя стена)
                image = load_image("Slice 67.png")
            elif i == 380:  # левый нижний угол обоев (передняя стена)
                image = load_image("Slice 81.png")
            elif i == 399:  # правый нижний угол обоев (передняя стена)
                image = load_image("Slice 85.png")
            elif i == 139:  # правый нижний угол обоев (задняя стена)
                image = load_image("Slice 69.png")
            elif i % 10 == 9 and (i + 1) / 10 % 2 == 0 and 150 < i < 400:  # правая стена рядом с полом
                image = load_image("Slice 75.png")
            elif i / 10 % 2 == 0 and 120 < i < 400:  # левая стена рядом с полом
                image = load_image("Slice 71.png")
            elif i / 10 % 2 == 0:  # левая стена рядом со стеной
                image = load_image("Slice 72.png")
            elif i % 10 == 9 and (i + 1) / 10 % 2 == 0 and 20 < i < 140:  # правая стена рядом со стеной
                image = load_image("Slice 74.png")
            elif i % 10 != 0 and 20 < i < 120:  # общий тон задней стены
                image = load_image("Slice 68.png")
            elif i % 10 != 0 and 120 < i < 140 and i != 130:  # нижний край стены (задняя стена)
                image = load_image("Slice 73.png")
            elif i == 386:  # левый угол передней стены у двери
                image = load_image("Slice 82.png")
            elif 380 < i < 387 or 389 < i < 399:  # нижний край стены (передняя стена)
                image = load_image("Slice 83.png")
            elif i == 389:  # правый угол передней стены у двери
                image = load_image("Slice 84.png")
            elif i % 10 != 0 and 140 < i < 400:  # пол
                image = load_image("Slice 96.png")
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
        # Прошлая дверь
        self.door_sprite3 = pygame.sprite.Sprite()
        image = load_image('Slice 96.png')
        self.door_sprite3.image = image
        self.door_sprite3.rect = self.door_sprite3.image.get_rect(topleft=(192, 480))
        group.add(self.door_sprite3)
        self.door_sprite3 = pygame.sprite.Sprite()
        image = load_image('Slice 96.png')
        self.door_sprite3.image = image
        self.door_sprite3.rect = self.door_sprite3.image.get_rect(topleft=(216, 480))
        group.add(self.door_sprite3)
        # Новая дверь
        self.door_sprite4 = pygame.sprite.Sprite()
        image = load_image('door.png')
        self.door_sprite4.image = image
        self.door_sprite4.rect = self.door_sprite4.image.get_rect(topleft=(256, 100))
        group.add(self.door_sprite4)

    def get_door_sprite3(self):
        return self.door_sprite3

    def get_door_sprite4(self):
        return self.door_sprite4


class Creature(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("Idle Front.png")
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200

    def update(self, *args):
        if args:
            if current_room == living_room and 170 < self.rect.x + args[0][0] < 205 \
                    and 400 < self.rect.y + args[0][1] < 450:
                self.rect.x += args[0][0]
                self.rect.y += args[0][1]
            elif current_room == corridor:
                if 218 < self.rect.x + args[0][0] < 253 and 400 < self.rect.y + args[0][1] < 450:
                    self.rect.x += args[0][0]
                    self.rect.y += args[0][1]
                elif 148 < self.rect.x + args[0][0] < 318 and 135 < self.rect.y + args[0][1] < 425:
                    self.rect.x += args[0][0]
                    self.rect.y += args[0][1]
            elif current_room == kitchen and 170 < self.rect.x + args[0][0] < 205 \
                    and 400 < self.rect.y + args[0][1] < 450:
                self.rect.x += args[0][0]
                self.rect.y += args[0][1]
            elif current_room != corridor:
                if 30 < self.rect.x + args[0][0] < 436 and 135 < self.rect.y + args[0][1] < 425:
                    self.rect.x += args[0][0]
                    self.rect.y += args[0][1]

    def check_interaction_door(self, door_sprite):
        # Проверяем, находится ли игрок рядом с дверью
        # if комната
        if self.rect.colliderect(door_sprite.rect):
            return True
        return False


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Organs')
    size = width, height = 524, 524
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()

    # Создайте спальню, гостиную, коридор
    living_room = LivingRoom(all_sprites)
    bedroom = Bedroom(all_sprites)
    corridor = Corridor(all_sprites)
    kitchen = Kitchen(all_sprites)
    first_fl = True  # Отрисовка нужной комнаты при создании

    current_room = bedroom
    player = Creature()
    all_sprites.add(player)

    FPS = 20
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        screen.fill('black')
        if first_fl:  # Отрисовка нужной комнаты при создании
            all_sprites.empty()  # Очищаем группу спрайтов
            bedroom.__init__(all_sprites)
            all_sprites.add(player)  # Добавляем игрока в новую комнату
            player.rect.center = (220, 180)  # Устанавливаем позицию игрока
            first_fl = False
        if keys[pygame.K_a]:
            all_sprites.update((-10, 0))
        elif keys[pygame.K_d]:
            all_sprites.update((10, 0))
        elif keys[pygame.K_w]:
            all_sprites.update((0, -10))
        elif keys[pygame.K_s]:
            all_sprites.update((0, 10))
        if keys[pygame.K_e] and not keys[pygame.K_s] and not keys[pygame.K_w]:
            # Проверяем взаимодействие с дверью
            if current_room == bedroom or current_room == living_room:
                if player.rect.colliderect(current_room.get_door_sprite().rect):
                    # Переход в другую комнату
                    if current_room == bedroom:
                        current_room = living_room
                        all_sprites.empty()  # Очищаем группу спрайтов
                        living_room.__init__(all_sprites)
                        all_sprites.add(player)  # Добавляем игрока в новую комнату
                        player.rect.center = (210, 470)  # Устанавливаем позицию игрока
                    elif current_room == living_room:
                        current_room = bedroom
                        all_sprites.empty()  # Очищаем группу спрайтов
                        bedroom.__init__(all_sprites)
                        all_sprites.add(player)  # Добавляем игрока в новую комнату
                        player.rect.center = (220, 160)  # Устанавливаем позицию игрока
            if current_room == living_room or current_room == corridor:
                if player.rect.colliderect(current_room.get_door_sprite2().rect):
                    # Переход в другую комнату
                    if current_room == corridor:
                        current_room = living_room
                        all_sprites.empty()  # Очищаем группу спрайтов
                        living_room.__init__(all_sprites)
                        all_sprites.add(player)  # Добавляем игрока в новую комнату
                        player.rect.center = (275, 160)  # Устанавливаем позицию игрока
                    elif current_room == living_room:
                        current_room = corridor
                        all_sprites.empty()  # Очищаем группу спрайтов
                        corridor.__init__(all_sprites)
                        all_sprites.add(player)  # Добавляем игрока в новую комнату
                        player.rect.center = (258, 470)  # Устанавливаем позицию игрока
            if current_room == corridor or current_room == kitchen:
                if player.rect.colliderect(current_room.get_door_sprite3().rect):
                    # Переход в другую комнату
                    if current_room == corridor:
                        current_room = kitchen
                        all_sprites.empty()  # Очищаем группу спрайтов
                        kitchen.__init__(all_sprites)
                        all_sprites.add(player)  # Добавляем игрока в новую комнату
                        player.rect.center = (210, 470)  # Устанавливаем позицию игрока
                    elif current_room == kitchen:
                        current_room = corridor
                        all_sprites.empty()  # Очищаем группу спрайтов
                        corridor.__init__(all_sprites)
                        all_sprites.add(player)  # Добавляем игрока в новую комнату
                        player.rect.center = (260, 160)  # Устанавливаем позицию игрока

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

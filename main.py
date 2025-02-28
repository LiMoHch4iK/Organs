import os
import sqlite3

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QRadioButton, QMenuBar, QStatusBar, QPushButton, \
    QApplication

from start_screen import *


class Test(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(700, 340)  # Устанавливаем фиксированный размер окна
        self.setWindowTitle("Тест")

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.layout = QVBoxLayout(self.centralwidget)

        self.question = QLabel("TextLabel", self)
        self.layout.addWidget(self.question)

        self.variant1 = QRadioButton("RadioButton", self)
        self.variant2 = QRadioButton("RadioButton", self)
        self.variant3 = QRadioButton("RadioButton", self)
        self.variant4 = QRadioButton("RadioButton", self)
        self.layout.addWidget(self.variant1)
        self.layout.addWidget(self.variant2)
        self.layout.addWidget(self.variant3)
        self.layout.addWidget(self.variant4)

        self.pushButton = QPushButton("Проверить", self)
        self.layout.addWidget(self.pushButton)

        self.label_result = QLabel("", self)  # Лейбл для отображения результата
        self.layout.addWidget(self.label_result)

        self.label_errors = QLabel("Ошибки: 0", self)  # Лейбл для отображения ошибок
        self.layout.addWidget(self.label_errors)

        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        if current_room_for_test == ['bedroom']:
            self.current_question_index = 0  # Индекс текущего вопроса
            self.total_questions = 5  # Число вопросов в базе
        elif current_room_for_test == ['living_room']:
            self.current_question_index = 5  # Индекс текущего вопроса
            self.total_questions = 10  # Число вопросов в базе
        self.errors_count = 0  # Количество ошибок
        self.load_question()

        self.pushButton.clicked.connect(self.check_answer)

    def load_question(self):
        con = sqlite3.connect('organs_test.sqlite')
        cur = con.cursor()
        question = cur.execute("""
        SELECT question FROM test 
        WHERE id = ? """, (self.current_question_index + 1,)).fetchone()
        self.question.setText(question[0])

        variants = cur.execute("""
        SELECT variant FROM variants 
        WHERE id =(SELECT variants FROM test 
        WHERE id = ?)""", (self.current_question_index + 1,)).fetchone()
        variants = variants[0].split(', ')
        self.variant1.setText(variants[0].split(',')[0])
        self.variant2.setText(variants[1].split(',')[0])
        self.variant3.setText(variants[2].split(',')[0])
        self.variant4.setText(variants[3].split(',')[0])

        con.close()

    def check_answer(self):
        con = sqlite3.connect('organs_test.sqlite')
        cur = con.cursor()

        if self.variant1.isChecked():
            answer = self.variant1.text()
        elif self.variant2.isChecked():
            answer = self.variant2.text()
        elif self.variant3.isChecked():
            answer = self.variant3.text()
        elif self.variant4.isChecked():
            answer = self.variant4.text()
        else:
            answer = ''

        right_answer = cur.execute("""
                   SELECT answer FROM test 
                   WHERE id = ? """, (self.current_question_index + 1,)).fetchone()
        con.close()
        if right_answer[0] == answer:
            self.label_result.setText('Верно')
        else:
            self.label_result.setText('Неверно')
            self.errors_count += 1
            self.label_errors.setText(f"Ошибки: {self.errors_count}")

        self.current_question_index += 1  # Переходим к следующему вопросу
        if self.current_question_index < self.total_questions:
            self.load_question()
        else:
            self.pushButton.setEnabled(False)  # Отключаем кнопку, если тест завершен
            if self.errors_count != 0:
                self.label_result.setText(
                    'Тест завершен! Проход в следующую комнату закрыт. Возвращайтесь когда выучите тему!')
            else:
                self.label_result.setText(
                    'Тест завершен! Проходите в следующую комнату и найдите орган.')
                if current_room == bedroom:
                    current_room_for_test.clear()
                    current_room_for_test.append('living_room')
                    finish_test.append('bedroom')
                    all_sprites.empty()  # Очищаем группу спрайтов
                    living_room.__init__(all_sprites)
                    all_sprites.add(player)  # Добавляем игрока в новую комнату
                    player.rect.center = (210, 470)  # Устанавливаем позицию игрока
                if current_room == living_room:
                    current_room_for_test.clear()
                    current_room_for_test.append('corridor')
                    finish_test.append('living_room')
                    all_sprites.empty()  # Очищаем группу спрайтов
                    corridor.__init__(all_sprites)
                    all_sprites.add(player)  # Добавляем игрока в новую комнату
                    player.rect.center = (258, 470)  # Устанавливаем позицию игрока


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
        self.furniture = set()
        self.bed_sprite = pygame.sprite.Sprite()
        image = load_image('bed.png')
        self.bed_sprite.image = image
        self.bed_sprite.rect = self.bed_sprite.image.get_rect(topleft=(330, 150))
        group.add(self.bed_sprite)
        self.furniture.add(self.bed_sprite)
        self.paint_sprite = pygame.sprite.Sprite()
        image = load_image('paint.png')
        self.paint_sprite.image = image
        self.paint_sprite.rect = self.paint_sprite.image.get_rect(topleft=(360, 45))
        group.add(self.paint_sprite)
        self.furniture.add(self.paint_sprite)
        self.chest_sprite = pygame.sprite.Sprite()
        image = load_image('chest.png')
        self.chest_sprite.image = image
        self.chest_sprite.rect = self.chest_sprite.image.get_rect(topleft=(275, 160))
        group.add(self.chest_sprite)
        self.furniture.add(self.chest_sprite)
        self.table_sprite = pygame.sprite.Sprite()
        image = load_image('table.png')
        self.table_sprite.image = image
        self.table_sprite.rect = self.table_sprite.image.get_rect(topleft=(415, 325))
        group.add(self.table_sprite)
        self.furniture.add(self.table_sprite)
        self.book = pygame.sprite.Sprite()
        image = load_image('book.png')
        self.book.image = image
        self.book.rect = self.book.image.get_rect(topleft=(420, 330))
        group.add(self.book)
        self.chair_sprite = pygame.sprite.Sprite()
        image = load_image('chair.png')
        self.chair_sprite.image = image
        self.chair_sprite.rect = self.chair_sprite.image.get_rect(topleft=(360, 350))
        group.add(self.chair_sprite)
        self.furniture.add(self.chair_sprite)
        self.wardrobe_sprite = pygame.sprite.Sprite()
        image = load_image('wardrobe.png')
        self.wardrobe_sprite.image = image
        self.wardrobe_sprite.rect = self.wardrobe_sprite.image.get_rect(topleft=(45, 80))
        group.add(self.wardrobe_sprite)
        self.furniture.add(self.wardrobe_sprite)
        self.easel_sprite = pygame.sprite.Sprite()
        image = load_image('easel.png')
        self.easel_sprite.image = image
        self.easel_sprite.rect = self.easel_sprite.image.get_rect(topleft=(90, 280))
        group.add(self.easel_sprite)
        self.furniture.add(self.easel_sprite)
        self.chair1_sprite = pygame.sprite.Sprite()
        image = load_image('chair1.png')
        self.chair1_sprite.image = image
        self.chair1_sprite.rect = self.chair1_sprite.image.get_rect(topleft=(95, 370))
        group.add(self.chair1_sprite)
        self.furniture.add(self.chair1_sprite)

    def get_door_sprite(self):
        return self.door1_sprite

    def get_book_sprite(self):
        return self.book


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
        self.furniture = set()
        if not eyes_fl:
            self.eyes = pygame.sprite.Sprite()
            image = load_image('eyes.png')
            self.eyes.image = image
            self.eyes.rect = self.eyes.image.get_rect(topleft=(100, 390))
            group.add(self.eyes)
            self.furniture.add(self.eyes)
        self.sofa_sprite = pygame.sprite.Sprite()
        image = load_image('sofa.png')
        self.sofa_sprite.image = image
        self.sofa_sprite.rect = self.sofa_sprite.image.get_rect(topleft=(48, 140))
        group.add(self.sofa_sprite)
        self.furniture.add(self.sofa_sprite)
        self.TV = pygame.sprite.Sprite()
        image = load_image('TV.png')
        self.TV.image = image
        self.TV.rect = self.TV.image.get_rect(topleft=(340, 100))
        group.add(self.TV)
        self.cushion1 = pygame.sprite.Sprite()
        image = load_image('cushion.png')
        self.cushion1.image = image
        self.cushion1.rect = self.cushion1.image.get_rect(topleft=(340, 220))
        group.add(self.cushion1)
        self.furniture.add(self.cushion1)
        self.cushion2 = pygame.sprite.Sprite()
        image = load_image('cushion.png')
        self.cushion2.image = image
        self.cushion2.rect = self.cushion2.image.get_rect(topleft=(415, 235))
        group.add(self.cushion2)
        self.furniture.add(self.cushion2)
        self.piano = pygame.sprite.Sprite()
        image = load_image('piano.png')
        self.piano.image = image
        self.piano.rect = self.piano.image.get_rect(topleft=(320, 330))
        group.add(self.piano)
        self.furniture.add(self.piano)
        self.table1 = pygame.sprite.Sprite()
        image = load_image('table1.png')
        self.table1.image = image
        self.table1.rect = self.table1.image.get_rect(topleft=(53, 210))
        group.add(self.table1)
        self.furniture.add(self.table1)
        self.picture = pygame.sprite.Sprite()
        image = load_image('picture1.png')
        self.picture.image = image
        self.picture.rect = self.picture.image.get_rect(topleft=(80, 70))
        group.add(self.picture)

    def get_door_sprite(self):
        return self.door_sprite1

    def get_door_sprite2(self):
        return self.door_sprite2

    def get_eyes(self):
        return self.eyes


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
        self.furniture = set()
        if not lungs:
            self.lungs = pygame.sprite.Sprite()
            image = load_image('eyes.png')
            self.lungs.image = image
            self.lungs.rect = self.lungs.image.get_rect(topleft=(300, 200))
            group.add(self.lungs)
            self.furniture.add(self.lungs)

    def get_lungs(self):
        return self.lungs

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
        self.furniture = set()

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
        self.mask = pygame.mask.from_surface(self.image)  # Создаем маску для игрока

    def update(self, *args):
        if args:
            if current_room == living_room and 185 < self.rect.x + args[0][0] < 220 \
                    and 400 < self.rect.y + args[0][1] < 450:
                self.rect.x += args[0][0]
                self.rect.y += args[0][1]
            elif current_room == corridor:
                if 230 < self.rect.x + args[0][0] < 268 and 400 < self.rect.y + args[0][1] < 450:
                    self.rect.x += args[0][0]
                    self.rect.y += args[0][1]
                elif 163 < self.rect.x + args[0][0] < 330 and 135 < self.rect.y + args[0][1] < 425:
                    self.rect.x += args[0][0]
                    self.rect.y += args[0][1]
            elif current_room == kitchen and 185 < self.rect.x + args[0][0] < 220 \
                    and 400 < self.rect.y + args[0][1] < 450:
                self.rect.x += args[0][0]
                self.rect.y += args[0][1]
            elif current_room != corridor:
                if 45 < self.rect.x + args[0][0] < 451 and 135 < self.rect.y + args[0][1] < 425:
                    self.rect.x += args[0][0]
                    self.rect.y += args[0][1]

    def main_update(self, furniture, *args):
        # Проверка столкновения с мебелью по маске
        original_position = self.rect.topleft
        all_sprites.update(*args)
        for item in furniture:
            item_mask = pygame.mask.from_surface(item.image)  # Создаем маску для мебели
            if pygame.sprite.collide_mask(self, item):
                self.rect.topleft = original_position
                return False
        self.rect.topleft = original_position
        return True


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Organs')
    size = width, height = 524, 524
    screen = pygame.display.set_mode(size)

    start_screen(screen)

    eyes_fl = False
    lungs = False

    all_sprites = pygame.sprite.Group()
    # Создайте спальню, гостиную, коридор
    living_room = LivingRoom(all_sprites)
    bedroom = Bedroom(all_sprites)
    corridor = Corridor(all_sprites)
    kitchen = Kitchen(all_sprites)
    first_fl = True  # Отрисовка нужной комнаты при создании

    current_room = bedroom
    current_room_for_test = ['bedroom']
    finish_test = []
    player = Creature(all_sprites)

    app = QApplication(sys.argv)

    FPS = 20
    clock = pygame.time.Clock()

    running = True
    while running:
        if current_room_for_test == ['living_room'] and current_room == bedroom:
            current_room = living_room
        if current_room_for_test == ['corridor'] and current_room == living_room:
            current_room = corridor
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    # Проверяем взаимодействие с дверью
                    if current_room == bedroom or current_room == living_room:
                        if current_room == bedroom:
                            # rect_book = (420, 330, 40, 35), но нужно сделать прибавку так как книга лежит на столе
                            if player.rect.colliderect((400, 330, 60, 35)):
                                pass  # тут будет текст книги
                        if player.rect.colliderect(current_room.get_door_sprite().rect):
                            # Переход в другую комнату
                            if current_room == bedroom:
                                if 'bedroom' not in finish_test:
                                    window = Test()
                                    window.show()
                                else:
                                    current_room_for_test.clear()
                                    current_room = living_room
                                    all_sprites.empty()  # Очищаем группу спрайтов
                                    living_room.__init__(all_sprites)
                                    all_sprites.add(player)  # Добавляем игрока в новую комнату
                                    player.rect.center = (210, 470)  # Устанавливаем позицию игрок
                            elif current_room == living_room:
                                current_room_for_test.clear()
                                current_room = bedroom
                                all_sprites.empty()  # Очищаем группу спрайтов
                                bedroom.__init__(all_sprites)
                                all_sprites.add(player)  # Добавляем игрока в новую комнату
                                player.rect.center = (220, 160)  # Устанавливаем позицию игрока
                    if current_room == living_room or current_room == corridor:
                        if current_room == living_room:
                            if not eyes_fl:
                                if player.rect.colliderect(living_room.get_eyes().rect):
                                    eyes_fl = True
                                    all_sprites.empty()  # Очищаем группу спрайтов
                                    living_room.__init__(all_sprites)
                                    all_sprites.add(player)  # Добавляем игрока в новую комнату
                                    player.rect.move(player.rect.topleft)  # Устанавливаем позицию игрока
                        elif current_room == corridor:
                            if not lungs:
                                if player.rect.colliderect(corridor.get_lungs().rect):
                                    lungs = True
                                    all_sprites.empty()  # Очищаем группу спрайтов
                                    corridor.__init__(all_sprites)
                                    all_sprites.add(player)  # Добавляем игрока в новую комнату
                                    player.rect.move(player.rect.topleft)  # Устанавливаем позицию игрока
                        if player.rect.colliderect(current_room.get_door_sprite2().rect):
                            # Переход в другую комнату
                            if current_room == corridor:
                                current_room_for_test.clear()
                                current_room = living_room
                                all_sprites.empty()  # Очищаем группу спрайтов
                                living_room.__init__(all_sprites)
                                all_sprites.add(player)  # Добавляем игрока в новую комнату
                                player.rect.center = (275, 160)  # Устанавливаем позицию игрока
                            elif current_room == living_room:
                                if 'living_room' not in finish_test:
                                    current_room_for_test = ['living_room']
                                    window = Test()
                                    window.show()
                                else:
                                    current_room_for_test.clear()
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
                                current_room_for_test.clear()
                                current_room = corridor
                                all_sprites.empty()  # Очищаем группу спрайтов
                                corridor.__init__(all_sprites)
                                all_sprites.add(player)  # Добавляем игрока в новую комнату
                                player.rect.center = (260, 160)  # Устанавливаем позицию игрока

        keys = pygame.key.get_pressed()
        screen.fill('black')
        if first_fl:  # Отрисовка нужной комнаты при создании
            all_sprites.empty()  # Очищаем группу спрайтов
            bedroom.__init__(all_sprites)
            all_sprites.add(player)  # Добавляем игрока в новую комнату
            player.rect.center = (220, 180)  # Устанавливаем позицию игрока
            first_fl = False

            # Обработка клавиш
        if keys[pygame.K_a]:
            if player.main_update(current_room.furniture, (-10, 0)):
                all_sprites.update((-10, 0))
        elif keys[pygame.K_d]:
            if player.main_update(current_room.furniture, (10, 0)):
                all_sprites.update((10, 0))
        elif keys[pygame.K_w]:
            if player.main_update(current_room.furniture, (0, -10)):
                all_sprites.update((0, -10))
        elif keys[pygame.K_s]:
            if player.main_update(current_room.furniture, (0, 10)):
                all_sprites.update((0, 10))

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

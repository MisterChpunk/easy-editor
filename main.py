""" Необходимые модули """
import os

from PIL import Image, ImageFilter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog  # Диалог открытия файлов (и папок)
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from qt_material import apply_stylesheet

""" Приложение """
# объект приложения
app = QApplication([])
apply_stylesheet(app, theme="light_blue.xml")  # тема для приложения


""" Интерфейс приложения """
# объект окна
win = QWidget()
# задаем параметры
win.resize(700, 600)
win.setWindowTitle("Easy Editor")

# # виджеты окна приложения

# кнопка выбора папки
btn_dir = QPushButton("Папка")

# виджет надписи, где будет
# отображаться выбранное изображений
lb_image = QLabel("Картинка")

# окно списка изображений
list_files = QListWidget()

# кнопки для фильтров
btn_left = QPushButton("Лево")
btn_right = QPushButton("Право")
btn_flip = QPushButton("Зеркало")
btn_sharp = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")

# # размещение виджетов по лэйаутам

# первый "столбец"-лэйаут
col1 = QVBoxLayout()
col1.addWidget(btn_dir)  # кнопка выбора папки
col1.addWidget(list_files)  # список изображений

# второй "столбец"-лэйаут
col2 = QVBoxLayout()
col2.addWidget(lb_image)  # виджет изображения

# "линия"-лэйаут с кнопками для фильтров
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

# главная "линия"-лэйаут окна
# на неё добавляются 2 "столбца"-лэйаута
row = QHBoxLayout()
row.addLayout(col1, 20)  # первый шириной 20%
row.addLayout(col2, 80)  # второй шириной 80%

# прикрепляем линию на окно
win.setLayout(row)

# рабочая папка
workdir = ""


# функция выбора папки
def chooseWorkdir():
    global workdir
    # вызываем окно выбора папки и запоминаем выбраннную
    workdir = QFileDialog.getExistingDirectory()


# функция для фильтрации списка файлов files
# по расширенияем extensions
# (чтобы в списке файлов были только изображения)
def filter(files, extensions):
    result = []  # финальный список файлов

    # перебираем все названия файлов
    for filename in files:
        # перебираем все расширения
        for ext in extensions:
            # если файл имеет какое-то расширение
            if filename.endswith(ext):
                # добавляем его в список
                result.append(filename)
    return result  # возвращаем готовый список


# функция для отображения списка изображений
def showFilenameList():
    extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]  # список нужных расширений
    chooseWorkdir()  # запускаем выбор рабочей папки
    filenames = filter(
        os.listdir(workdir), extensions
    )  # получаем отфильтрованный список изображений
    list_files.clear()  # очищаем окно списка изображений
    for filename in filenames:  # добавляем все изображения в окно списка
        list_files.addItem(filename)


# подключаем кнопку выбора директории к функции
btn_dir.clicked.connect(showFilenameList)


""" Класс для обработки изображений """


class ImageProcessor:
    # конструктор, где задаются пустые свойства
    def __init__(self):
        self.image = None  # свойство с изображением
        self.dir = None  # свойство с папкой
        self.filename = None  # свойство с названием файла
        self.save_dir = "Modified/"  # свойство с названием папки для сохранения

    # метод для открытия изображения
    def loadImage(self, dir, filename):
        self.dir = dir  # папка с изображением
        self.filename = filename  # название изображения
        image_path = os.path.join(
            dir, filename
        )  # соединяем путь к папке с названием файла
        self.image = Image.open(image_path)  # открываем изображение по этому пути

    # метод для отображения изображения
    def showImage(self, path):
        lb_image.hide()  # прячем виджет для изображения
        pixmapimage = QPixmap(path)  # открываем изображение для PyQt по пути
        w, h = lb_image.width(), lb_image.height()  # получаем размеры изображения
        pixmapimage = pixmapimage.scaled(
            w, h, Qt.KeepAspectRatio
        )  # уменьшаем изображение без нарушения пропорций
        lb_image.setPixmap(pixmapimage)  # устанавливаем изображение
        lb_image.show()  # показываем виджет для изображения

    # метод для сохранения обработанной копии файла
    def saveImage(self):
        # сохраняет копию файла в подпапке Modified
        path = os.path.join(
            self.dir, self.save_dir
        )  # генерируем путь к папке для сохранений

        # если этого пути нет или этот путь не является папкой
        if not (os.path.exists(path) or os.path.isdir(path)):
            # создаем папку для сохранений
            os.mkdir(path)

        image_path = os.path.join(path, self.filename)  # генерируем путь для сохранения
        self.image.save(image_path)  # сохраняем

    # метод для черно-белого фильтра
    def do_bw(self):
        self.image = self.image.convert("L")  # переводим изображение в ЧБ
        self.saveImage()  # сохраняем его
        image_path = os.path.join(
            self.dir, self.save_dir, self.filename
        )  # генерируем путь для сохранения
        self.showImage(image_path)  # отображаем обработанное изображение

    # метод для поворота налево
    def do_left(self):
        self.image = self.image.transpose(
            Image.ROTATE_90
        )  # поворачиваем изображение налево (налево 90 градусов)
        self.saveImage()  # сохраняем его
        image_path = os.path.join(
            self.dir, self.save_dir, self.filename
        )  # генерируем путь для сохранения
        self.showImage(image_path)  # отображаем обработанное изображение

    # метод для поворота направо
    def do_right(self):
        self.image = self.image.transpose(
            Image.ROTATE_270
        )  # поворачиваем изображение направо (налево 270 градусов)
        self.saveImage()  # сохраняем его
        image_path = os.path.join(
            self.dir, self.save_dir, self.filename
        )  # генерируем путь для сохранения
        self.showImage(image_path)  # отображаем обработанное изображение

    # метод для отзеркаливания изображения
    def do_flip(self):
        self.image = self.image.transpose(
            Image.FLIP_LEFT_RIGHT
        )  # отзеркаливаем изображение
        self.saveImage()  # сохраняем его
        image_path = os.path.join(
            self.dir, self.save_dir, self.filename
        )  # генерируем путь для сохранения
        self.showImage(image_path)  # отображаем обработанное изображение

    # метод для наведения резкости
    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)  # наводим резкость
        self.saveImage()  # сохраняем его
        image_path = os.path.join(
            self.dir, self.save_dir, self.filename
        )  # генерируем путь для сохранения
        self.showImage(image_path)  # отображаем обработанное изображение


# функция для выбора картинки
def showChosenImage():
    # если выбран какой-то элемент в окне списка изображений
    if list_files.currentRow() >= 0:
        filename = list_files.currentItem().text()  # получаем название изображения
        workimage.loadImage(workdir, filename)  # открываем его
        image_path = os.path.join(workdir, filename)  # получаем путь к изображению
        workimage.showImage(image_path)  # отображаем изображение в окне приложения


# экземпляр рабочей картинки
workimage = ImageProcessor()

# подключаем к списку изображений функцию для выбора
list_files.currentRowChanged.connect(showChosenImage)

# подключаем к кнопкам для инструментов функции
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)


# показываем окно
win.show()

# запускаем приложение
app.exec_()

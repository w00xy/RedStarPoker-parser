import csv
import subprocess
import time
from datetime import datetime

import psutil
import pygetwindow as pw
import pytesseract
from PIL import ImageGrab, Image

from config import WAIT_TIME, CASINO_PATH, WINDOW_TITLE, TESSERACT_PATH


class Logger:
    def __init__(self, prefix=None):
        self.prefix = prefix

    def log(self, data: str):
        if self.prefix:
            print(f"{self.prefix} {data}")
        else:
            print(data)

    def input(self, text: str):
        if self.prefix:
            return input(f"{self.prefix} {text}")
        else:
            return input(text)


class Casino:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.screen_path = "temp/screenshot.png"
        self.processes = ["casino.exe", "PokerClient.exe"]

    def open_window(self):
        subprocess.Popen(self.file_path)

    def get_screenshot(self, window_title: str):
        # Ищем окно по его названию
        windows = pw.getWindowsWithTitle(window_title)
        if not windows:
            print(f"Окно с названием {window_title} не найдено!")
            return None

        window = windows[1]

        # Активируем окно
        window.activate()
        time.sleep(5)  # Даем время на активацию окна

        # Координаты окна
        left, top, right, bottom = window.left, window.top, window.right, window.bottom

        # Захватываем скриншот окна
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

        # Сохраняем скриншот
        screenshot.save(self.screen_path)

        return screenshot

    def get_online(self,):
        # Координаты для обрезки области с числом игроков на основе окна приложения
        img = Image.open(self.screen_path)

        left = 230  # уточните по вашему изображению
        top = img.height - 30  # чуть выше, чем нижняя часть
        right = 315  # уточните
        bottom = img.height  # чуть выше нижней полосы
        cropped_img = img.crop((left, top, right, bottom))

        cropped_img.save("temp/cropped_online_players.png")

        online_text = pytesseract.image_to_string(cropped_img)

        # Парсим число игроков
        online_players = ''.join(filter(str.isdigit, online_text))

        return online_players

    def close(self,):
        for proc in psutil.process_iter():
            for proc_name in self.processes:
                if proc.name() == proc_name:
                    proc.terminate()

    @staticmethod
    def save_to_csv(online_players):
        # Получаем текущее время
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Открываем файл в режиме добавления строк
        with open('online_log.csv', mode='a', encoding="UTF-8", newline="") as file:
            writer = csv.writer(file, delimiter=";")

            # Записываем текущую дату и время и число игроков
            writer.writerow([current_time, online_players])



def try_parse_casino():

    logger = Logger("[LOG]")

    # необходимо для правильной работы библиотеки pytesseract для распознования текста
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    casino_path = CASINO_PATH
    window_title = WINDOW_TITLE

    # Создаем объект казино
    casino = Casino(casino_path)
    try:
        # Открываем приложение казино
        try:
            casino.open_window()
            logger.log("Открыли окно казино")
        except Exception as e:
            logger.log(f"Ошибка не смогли открыть окно казино: {e}")

        # Ждем несколько секунд, чтобы окно точно загрузилось
        time.sleep(20)

        # Делаем скриншот окна
        casino.get_screenshot(window_title)

        # парсим число онлайна
        logger.log("Пробуем спарсить онлайн")
        online = casino.get_online()
        logger.log(f"Онлайн: {online} | Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        casino.save_to_csv(online)
        logger.log("Записываем онлайн в csv")

        casino.close()
        logger.log("Закрыли казино")
    except Exception as e:
        try:
            casino.close()
            logger.log("Закрываем окно")
        except ProcessLookupError:
            pass

        logger.log(f"Произошла ошибка: {str(e)}")


def main():
    # Запускаем программу в бесконечном цикле с интервалом 60 секунд
    while True:
        try_parse_casino()

        # Ожидание перед следующим запуском
        time.sleep(WAIT_TIME)


if __name__ == "__main__":
    main()

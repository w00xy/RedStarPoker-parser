# Casino Online Logger

## Описание

Проект `Casino Online Logger` представляет собой Python-скрипт, который запускает клиент онлайн-казино (например, RedStar Poker), делает скриншот окна программы, извлекает число игроков, находящихся онлайн, и сохраняет эти данные в CSV файл с текущей датой и временем. Программа работает в цикле, обновляя данные каждый час.

## Требования

Для работы проекта необходимо установить следующие зависимости:

- Python 3.9 - 3.x
- Модули Python:
  - `pillow` (для обработки изображений)
  - `pygetwindow` (для управления окнами)
  - `pytesseract` (для распознавания текста с изображений)
  - `psutil` (для работы с процессами)
  - `csv` (для работы с CSV файлами)
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (для распознавания текста)
- Клиент казино (RedStar Poker)

### Установка Tesseract
[Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (для распознавания текста)

### Заполнить config.py
```python
TESSERACT_PATH = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # Базовый путь
WAIT_TIME = 3600  # Задержка между парсингом (указывается в секундах)
CASINO_PATH = "C:\\Program Files (x86)\\Red Star Poker\\casino.exe"  # Путь к файлу казино
WINDOW_TITLE = "RedStar Poker"  # Название окна (Менять не нужно)
```

### Создание вирутального окружения python
```bash
python -m venv venv
```

### Установка необходимых пакетов

```bash
pip install -r requirements.txt
```

### Запуск программы
```bash
python main.py
```

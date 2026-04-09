# -*- coding: utf-8 -*-

import sys
import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Шлях до скрипта, який потрібно запускати
# os.path.dirname(__file__) отримує каталог, де знаходиться цей файл (watch_posts.py)
SCRIPT_TO_RUN = os.path.join(os.path.dirname(__file__), "generate_posts_index.py")

# Каталог для моніторингу змін. Припускаємо, що він знаходиться в тому ж каталозі, що й скрипт.
DIRECTORY_TO_MONITOR = os.path.join(os.path.dirname(__file__), "posts")

class PostUpdateHandler(FileSystemEventHandler):
    """Обробник подій для моніторингу змін у каталозі з постами."""
    
    def on_modified(self, event):
        # Ігноруємо каталоги та інші файли, крім .md
        if not event.is_directory and event.src_path.endswith(".md"):
            print(f"✅ Виявлено зміну у файлі: {event.src_path}. Запускаємо скрипт...")
            self.run_script()

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            print(f"➕ Виявлено новий файл: {event.src_path}. Запускаємо скрипт...")
            self.run_script()

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            print(f"❌ Виявлено видалення файлу: {event.src_path}. Запускаємо скрипт...")
            self.run_script()

    def run_script(self):
        """Запускає скрипт generate_posts_index.py."""
        try:
            # Використовуємо sys.executable, щоб гарантувати запуск тим же інтерпретатором Python,
            # що й цей скрипт-спостерігач.
            result = subprocess.run(
                [sys.executable, SCRIPT_TO_RUN],
                capture_output=True,
                text=True,
                encoding='utf-8' # Явно вказуємо кодування для коректного виведення
            )
            print("🚀 Скрипт завершив роботу.")
            if result.stdout:
                print("--- Вивід скрипта ---
", result.stdout)
            if result.stderr:
                print("--- Помилки скрипта ---
", result.stderr)
            if result.returncode != 0:
                print(f"❗ Скрипт завершився з помилкою (код виходу: {result.returncode}).")
        except FileNotFoundError:
            print(f"⛔ Помилка: Не вдалося знайти інтерпретатор Python '{sys.executable}' або скрипт '{SCRIPT_TO_RUN}'.")
        except Exception as e:
            print(f"⛔ Виникла неочікувана помилка під час запуску скрипта: {e}")

if __name__ == "__main__":
    # Перевірка, чи існують необхідні файли та каталоги
    if not os.path.exists(DIRECTORY_TO_MONITOR):
        print(f"⛔ Помилка: Каталог для моніторингу '{DIRECTORY_TO_MONITOR}' не існує.")
        sys.exit(1)
        
    if not os.path.exists(SCRIPT_TO_RUN):
        print(f"⛔ Помилка: Скрипт '{SCRIPT_TO_RUN}' не знайдено.")
        sys.exit(1)

    print(f"👀 Моніторинг каталогу: {DIRECTORY_TO_MONITOR}")
    print(f"🚀 Скрипт, що запускатиметься при змінах: {SCRIPT_TO_RUN}")
    print("Натисніть Ctrl+C для зупинки.")

    event_handler = PostUpdateHandler()
    observer = Observer()
    # `recursive=True` означає, що будуть відстежуватися зміни і у підкаталогах posts/
    observer.schedule(event_handler, DIRECTORY_TO_MONITOR, recursive=True) 
    observer.start()

    try:
        while True:
            time.sleep(1) # Короткий сон, щоб не навантажувати процесор
    except KeyboardInterrupt:
        print("
✋ Зупинка моніторингу...")
        observer.stop()
    observer.join()
    print("✅ Моніторинг зупинено.")

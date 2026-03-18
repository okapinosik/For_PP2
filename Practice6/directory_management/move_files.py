from pathlib import Path
import shutil
import os
path = Path("parent/child/grandchild")
path.mkdir(parents=True, exist_ok=True)
print("Список объектов:", os.listdir("."))
# Перемещение/копирование между папками
# Создадим файл и переместим его в созданную ранее папку
test_file = Path("test.txt")
test_file.touch() # создаем пустой файл
shutil.move("test.txt", "parent/child/test_moved.txt")
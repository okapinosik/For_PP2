from pathlib import Path
import os

#  Создание вложенных директорий
path = Path("parent/child/grandchild")
path.mkdir(parents=True, exist_ok=True)

# Список файлов и папок в текущей директории
print("Список объектов:", os.listdir("."))
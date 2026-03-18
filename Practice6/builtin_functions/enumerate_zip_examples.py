from functools import reduce

nums = [1, 2, 3, 4, 5]

# 3. enumerate() и zip()
names = ["Alice", "Bob", "Charlie"]
# zip объединяет два списка в пары
for name, score in zip(names, nums):
    print(f"Игрок: {name}, Очки: {score}")

# enumerate добавляет индекс
for i, name in enumerate(names):
    print(f"Позиция {i}: {name}")

# 4. Проверка типов и конвертация
val = "100"
if isinstance(val, str): # Проверка типа
    num_val = int(val)   # Конвертация
    print(f"Тип изменен на: {type(num_val)}")
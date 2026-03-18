from functools import reduce

nums = [1, 2, 3, 4, 5]

# enumerate() и zip()
names = ["Alice", "Bob", "Charlie"]
# zip объединяет два списка в пары
for name, score in zip(names, nums):
    print(f"Игрок: {name}, Очки: {score}")

# enumerate добавляет индекс
for i, name in enumerate(names):
    print(f"Позиция {i}: {name}")

# Проверка типов и конвертация
val = "100"
if isinstance(val, str): 
    num_val = int(val)   
    print(f"Тип изменен на: {type(num_val)}")
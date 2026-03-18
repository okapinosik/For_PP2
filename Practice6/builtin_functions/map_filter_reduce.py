from functools import reduce

nums = [1, 2, 3, 4, 5]

# map() и filter()
squared = list(map(lambda x: x**2, nums))     
evens = list(filter(lambda x: x % 2 == 0, nums)) 
print(f"Квадраты: {squared}, Четные: {evens}")

# Агрегация с reduce()
total_sum = reduce(lambda x, y: x + y, nums)
print(f"Сумма всех чисел: {total_sum}")



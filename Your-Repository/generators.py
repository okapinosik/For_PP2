#1.Task
def square_generator(n):
    for i in range(n + 1):
        yield i * i
N = 5
for value in square_generator(N):
    print(value)
    
#2.Task
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield str(i)

n = int(input("Введите n: "))
print(",".join(even_numbers(n)))


#3.Task
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


n = 50
for number in divisible_by_3_and_4(n):
    print(number)
#4.Task
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


# Тест
for value in squares(3, 7):
    print(value)
#5.Task
def countdown(n):
    for i in range(n, -1, -1):
        yield i

for number in countdown(5):
    print(number)



""" The for loop actually creates an iterator object and executes the next() method for each loop. """
""" yield — это ключевое слово в Python, которое превращает обычную функцию в генератор. 
В отличие от return, который полностью завершает работу функции и возвращает результат, yield лишь приостанавливает её выполнение, отдаёт значение и «запоминает» состояние всех переменных.  
all classes have a function called __init__(), which allows you to do some initializing when the object is being created.

The __iter__() method acts similar, you can do operations (initializing etc.), but must always return the iterator object itself.

The __next__() method also allows you to do operations, and must return the next item in the sequence.
"""
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))





mystr = "banana"

for x in mystr:
  print(x)




def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1

ctr = fun(5)
for n in ctr:
    print(n)
    
    
    
    
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))


"""
1
2
3
4
5 
"""
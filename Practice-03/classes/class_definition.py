""" Python Classes/Objects
Python is an object oriented programming language.

Almost everything in Python is an object, with its properties and methods.

A Class is like an object constructor, or a "blueprint" for creating objects. """

class MyClass:
  x = 5
  
p1 = MyClass()
print(p1.x)

""" You can delete objects by using the del keyword:

Example
Delete the p1 object:
 """
del p1

p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)


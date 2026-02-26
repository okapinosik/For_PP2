import math
import random

#tasks
import math

# 1. Degree to radian
degree = int(input("Input degree: "))
radian = degree * math.pi / 180
print("Output radian:", round(radian, 6))

# 2. Area of trapezoid
height = int(input("\nHeight: "))
base1 = int(input("Base, first value: "))
base2 = int(input("Base, second value: "))
trapezoid_area = ((base1 + base2) / 2) * height
print("Expected Output:", trapezoid_area)

# 3. Area of regular polygon
n = int(input("\nInput number of sides: "))
a = int(input("Input the length of a side: "))
polygon_area = (n * a ** 2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", round(polygon_area))

# 4. Area of parallelogram
base = int(input("\nLength of base: "))
height_p = int(input("Height of parallelogram: "))
parallelogram_area = base * height_p
print("Expected Output:", float(parallelogram_area))


""" 
Key Constants: math.pi (3.14159), math.e (2.71828).
Key Functions:
math.sqrt(x): Square root.
math.ceil(x) / math.floor(x): Round up/down.
math.factorial(x): Factorial.
math.log(x, base): Logarithm.
math.sin(x), math.cos(x), math.tan(x): Trigonometry (radians).
Rounding: round(number, digits)



random.random()	Returns a random float in the range [0.0, 1.0) (inclusive of 0, exclusive of 1).

random.randint(a, b)	Returns a random integer N
 such that a<=N<=b
 (both inclusive).

random.shuffle(x)	Shuffles the elements of a list in place (modifies the original list) 
"""
print(random.random())
print(random.randint(1, 6)) # Dice roll
colors = ["red", "blue"]; print(random.choice(colors))
cards = [1, 2, 3]; random.shuffle(cards); print(cards)

a = abs(-7.25)

print(a)


c = pow(4, 3)

print(c)



p = math.pi

print(p)


x = math.ceil(1.4)
y = math.floor(1.4)

print(x) # returns 2
print(y) # returns 1
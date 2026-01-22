print("Hello")
print('Hello')

print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

a = "Hello"
print(a)

a1 = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a1)

a2 = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a2)



#sub theme slicing strings
b = "Hello, World!"
print(b[2:5])

b1 = "Hello, World!"
print(b1[:5])

c = "Hello, World!"
print(c[2:])

c1 = "Hello, World!"
print(c1[-5:-2])



#sub-theme modify strings
x = "Hello, World!"
print(x.upper())

x1 = "Hello, World!"
print(x1.lower())

y = " Hello, World! "
print(y.strip()) 



#sub theme concatenate strings
x2 = "Hello"
y1 = "World"
c1 = x2 + y1
print(c1)

x3 = "Hello"
y3 = "World"
c2 = x3 + " " + y3
print(c2)



#sub theme format strings

"""
age = 36

txt = "My name is John, I am " + age <- error
print(txt)  
"""

age = 36
txt = f"My name is John, I am {age}"
print(txt)

price = 59
txt1 = f"The price is {price} dollars"
print(txt1)

price = 59
txt2 = f"The price is {price} dollars"
print(txt2)

txt_ = f"The price is {20 * 59} dollars"
print(txt_)


#sub theme escape characters
txt3 = "We are the so-called \"Vikings\" from the north."
# txt = "We are the so-called "Vikings" from the north." <- error
import re
# 1. Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
def task1(s):
    pattern = r"^ab*$"
    return bool(re.match(pattern, s))

print("1:", task1("a"))       # True
print("1:", task1("ab"))      # True
print("1:", task1("abbb"))    # True
print("1:", task1("ac"))      # False


# 2. Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
def task2(s):
    pattern = r"^ab{2,3}$"
    return bool(re.match(pattern, s))

print("2:", task2("abb"))     # True
print("2:", task2("abbb"))    # True
print("2:", task2("abbbb"))   # False


# 3. Write a Python program to find sequences of lowercase letters joined with a underscore.
def task3(s):
    pattern = r"\b[a-z]+_[a-z]+\b"
    return re.findall(pattern, s)

print("3:", task3("hello_world test one_more_example A_B"))  



# 4. Write a Python program to find the sequences of one upper case letter followed by lower case letters.
def task4(s):
    pattern = r"\b[A-Z][a-z]+\b"
    return re.findall(pattern, s)

print("4:", task4("Hello world My Name is Python"))


# 5. Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
def task5(s):
    pattern = r"^a.*b$"
    return bool(re.match(pattern, s))

print("5:", task5("ab"))        # True
print("5:", task5("axxxb"))     # True
print("5:", task5("a12345b"))   # True
print("5:", task5("a12345c"))   # False


# 6. Write a Python program to replace all occurrences of space, comma, or dot with a colon.
def task6(s):
    pattern = r"[ ,.]"
    return re.sub(pattern, ":", s)

print("6:", task6("Python, is great. Really great"))



# 7. Write a python program to convert snake case string to camel case string.
def task7(s):
    return re.sub(r"_([a-zA-Z])", lambda m: m.group(1).upper(), s)

print("7:", task7("snake_case_string"))  



# 8. Write a Python program to split a string at uppercase letters.


def task8(s):
    pattern = r"[A-Z][a-z]*"
    return re.findall(pattern, s)

print("8:", task8("SplitThisStringAtUppercase"))  



# 9. Write a Python program to insert spaces between words starting with capital letters.
def task9(s):
    return re.sub(r"(?<!^)([A-Z])", r" \1", s)

print("9:", task9("InsertSpacesBetweenWords"))  



# 10. Write a Python program to convert a given camel case string to snake case.
def task10(s):
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()

print("10:", task10("camelCaseString"))  
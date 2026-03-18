# Создание и запись
with open("example.txt", "w", encoding="utf-8") as f:
    f.write("Первая строка данных \nВторая строка данных")
    
# Чтение и вывод
with open("example.txt", "r", encoding="utf-8") as f:
    print("Содержимое файла:", f.read())

""" "r" - Read - Default value. Opens a file for reading, error if the file does not exist

"a" - Append - Opens a file for appending, creates the file if it does not exist

"w" - Write - Opens a file for writing, creates the file if it does not exist

"x" - Create - Creates the specified file, returns an error if the file exists """

""" "t" - Text - Default value. Text mode

"b" - Binary - Binary mode (e.g. images) """

""" Syntax
To open a file for reading it is enough to specify the name of the file:

f = open("demofile.txt")
The code above is the same as:

f = open("demofile.txt", "rt") """

""" The open() function returns a file object, which has a read() method for reading the content of the file: """
f = open("demofile.txt")
print(f.read())

with open("demofile.txt") as f:
  print(f.read())
  
""" Close Files
It is a good practice to always close the file when you are done with it.

If you are not using the with statement, you must write a close statement in order to close the file:

Example
Close the file when you are finished with it: """

f = open("demofile.txt")
print(f.readline())
f.close()


""" By default the read() method returns the whole text, but you can also specify how many characters you want to return """

""" You can return one line by using the readline() method """


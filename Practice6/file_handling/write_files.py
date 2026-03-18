#  Добавление (append) и проверка
with open("example.txt", "a", encoding="utf-8") as f:
    f.write("\nНовая добавленная строка.")


""" To write to an existing file, you must add a parameter to the open() function:

"a" - Append - will append to the end of the file

"w" - Write - will overwrite any existing content """

""" Overwrite Existing Content
To overwrite the existing content to the file, use the w parameter:

Example
Open the file "demofile.txt" and overwrite the content: """

with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")

#open and read the file after the overwriting:
with open("demofile.txt") as f:
  print(f.read())
"""   
To create a new file in Python, use the open() method, with one of the following parameters:

"x" - Create - will create a file, returns an error if the file exists

"a" - Append - will create a file if the specified file does not exists

"w" - Write - will create a file if the specified file does not exists """
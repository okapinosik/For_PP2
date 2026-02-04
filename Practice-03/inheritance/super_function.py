""" Use the super() Function
Python also has a super() function that will make the child class inherit all the methods and properties from its parent: """

class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)
    

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def say_hello(self):
        print("안녕하세요! 제 이름은 {}입니다. {}살입니다.".format(self.name, self.age))

    def more(self):
        print("one more!")
        self.say_hello

person1 = Person("Alice", 20)
person2 = Person("Bob", 22)

person1.say_hello()
person2.say_hello()

person1.more()
person2.more()
print(person1.name, person1.age)
print(person2.name, person2.age)
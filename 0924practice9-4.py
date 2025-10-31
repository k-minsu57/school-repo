# 부모 클래스
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound
    
    def make_sound(self):
        # print(f"{self.name} makes a {self.sound} sound.")
        print("{0} makes a {1} sound".format(self.name, self.sound))
    
# 자식 클래스 (Animal 클래스 상속)
class Dog(Animal):
    def __init__(self, name, sound, breed):
        Animal.__init__(self, name, sound) # 부모 클래스의 __init__직접 호출
        self.breed = breed

    def info(self):
        print(f"{self.name} is a {self.breed} and it barks.")

# 자식 클래스 (Animal 클래스 상속)
class Cat(Animal):
    def __init__(self, name, sound, color):
        Animal.__init__(self, name, sound) # 부모 클래스의 __init__ 직접 호출
        self.color = color

    def info(self):
        print(f"{self.name} is a {self.color} cat and it meows.")

# 객체 생성
dog = Dog("Buddy", "Bark", "Golden Retriever")
cat = Cat("Whiskers", "meow", "black")

# 메서드 호출
dog.make_sound() # Buddy makes a bark sound.
dog.info()       # Buddy is a Golden Retriever and it barks

cat.make_sound() # Whiskers makes a meow sound.
cat.info()       # Whiskers is a black cat and it meows.
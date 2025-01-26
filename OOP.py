#Принцип Инкапсуляции
class Cat():
    def __init__(self, breed, color, age):
        self._breed = breed
        self._color = color
        self._age = age

    @property
    def breed(self):
        return self._breed

    @property
    def color(self):
        return self._color

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_age):
        if new_age > self._age:
            self._age = new_age
        return self._age

    def meow(self):
        print('Мяу!')

    def purr(self):
        print('Мррр!')

cat = Cat('Абиссинская', 'Рыжая', 4)
print(cat.breed)
print(cat.color)
print(cat.age)
cat.age = 5
print(cat.age)

#Принцип наследования
class HomeCat(Cat):
    def __init__(self, breed, color, age, owner, name):
        super().__init__(breed, color, age)
        self._owner = owner
        self._name = name

    @property
    def owner(self):
        return self._owner

    @property
    def name(self):
        return self._name

    def getTreat(self):
        print('Мяу-мяу')

my_cat = HomeCat('Сиамская', 'Белая', 3, 'Иван', 'Роза')

print(my_cat.owner)
print(my_cat.breed)
my_cat.getTreat()
my_cat.purr()

#Принцип полиморфизма
class Pcat:
    def sleep(self):
        print('Свернулся в клубок и сладко спит.')

class Parrot:
    def sleep(self):
        print('Сел на жердочку и уснул')

def homeSleep(animal):
    animal.sleep()

cat = Pcat()
parrot = Parrot()
homeSleep(cat)
homeSleep(parrot)

#Принцип абстракции
class Predator:
    def hunt(self):
        print('Охотится...')

class ACat(Predator):
    def __init__(self, name, color):
        super().__init__()
        self._name = name
        self._color = color

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

cat = ACat('Даниэла', 'Черный')
cat.hunt()

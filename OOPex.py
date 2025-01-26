class Drink():

    _volume = 200

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self._remains = self._volume

    def drink_info(self):
        print(f'Название: {self.name}. Стоимость: {self.price}. Объем: {self._volume}')

    def _is_enough(self, need):
        if self._remains >= need and self._remains > 0:
            return True
        print('Осталось недостаточно напитка')
        return False

    def sip(self):
        if self._is_enough(20) == True:
            self._remains -= 20
            print('Друг сделал глоток')
        else:
            print('Не хватает напитка для полноценного глотка')

    def small_sip(self):
        if self._is_enough(10) == True:
            self._remains -= 10
            print('Друг сделал маленький глоток')

    def drink_all(self):
        if self._is_enough(0) == True:
            self._remains = 0
            print('Друг выпил напиток залпом')

    def tell_price(self):
        print('Друг объявляет стоимость своего напитка')
        return self.price

coffee = Drink('Кофе', 300)
coffee.drink_info()
coffee.sip()

class Juice(Drink):

    __juice_name = 'сок'
    def __init__(self, price, taste):
        super().__init__(self.__juice_name, price)
        self.taste = taste

    def drink_info(self):
        print(f'Вкус сока: {self.taste}. Стоимость: {self.price}. Начальный объем: {self._volume}. Осталось: {self._remains}')

apple_juice = Juice(250, 'яблочный')
apple_juice.small_sip()
apple_juice.sip()
apple_juice.drink_info()

tea = Drink('чай', 500)
print(tea.tell_price())
beetlejuice = Juice(1988, 'жучиный')
print(beetlejuice.tell_price())

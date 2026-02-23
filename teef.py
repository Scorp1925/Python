try:
    x = 10 / 0
except ZeroDivisionError:
    x = 0
    print("Деление на ноль!")

try:
    # код, который может вызвать исключение
except (TypeError, ValueError):
    # обработка исключений типов TypeError и ValueError

try:
    # код, который может вызвать исключение
except TypeError:
    # обработка исключения
finally:
    # этот код будет выполнен в любом случае

class MyCustomException(Exception):
    pass

try:
    raise MyCustomException("Это мое собственное исключение!")
except MyCustomException as e:
    print(f"Обработано исключение: {e}")
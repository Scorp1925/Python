def my_decorator(func):
    def wrapper():
        print("Что-то происходит передв вызовом функции")
        func()
        print("Что-то происходит после вызова функции")
    return wrapper

@my_decorator
def say_hello():
    print("Привет, мир!")

say_hello()
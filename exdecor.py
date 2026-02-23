import time

def timing_decorator(func):
    def wrapper():
        start_time = time.time()
        func()
        end_time = time.time()
        print(f"Функция {func.__name__} выполнялась {end_time - start_time:.2f} секунд")
    return wrapper

@timing_decorator
def some_long_running_function():
    time.sleep(2)
    print("Функиця завершила работу")

some_long_running_function()

def logging(func):
    def log_function_called():
        print(f'Вызвана {func.__name__}')
        func()
    return log_function_called

@logging
def my_name():
	print('Крис')

@logging
def friends_name():
	print('Наруто')

my_name()
friends_name()
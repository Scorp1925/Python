import numpy as np

#Создадим массив
array = np.array([1, 2, 3, 4, 5])
print(f"Массив {array}")

#Базовые арифметические функции
array_plus_one = array + 1
print(f"Массив + 1 {array_plus_one}")

array_times_two = array * 2
print(f"Массив * 2 {array_times_two}")

array_minus_three = array - 3
print(f"Массив - 3 {array_minus_three}")

#Мультивекторы
vector_1 = np.array([1,2,3,])
vector_2 = np.array([4,5,6])
dot_product = np.dot(vector_1,vector_2)
print(f"Dpt product {dot_product}")

#Создание многомерного массива
matrix = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(f"Матрица {matrix}")

#Создание массива равномерно распределенными значениями в заданном диапазоне
arange_array = np.arange(0, 10, 2.3)
print(f"Arange array {arange_array}")

#Создание массива случайных чисел
random_array = np.random.rand(3,4)
print(f"Массив случайных чисел {random_array}")

#Вычисления минимального и максимального значений массива
min_value = np.min(array)
max_value = np.max(array)

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

# Конволюционная вевть
def create_convolutional_branch(input_shape):
    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Conv2D(32, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D())
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D())
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D())
    model.add(layers.Flatten())
    return model

# Полносвязный слой
def create_fully_connected_branch(input_shape):
    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Dense(16, activation='relu'))
    return model

# Определение входных данных
image_input_shape = (225, 225, 3)  # Вход для термограммы
sensor_input_shape = (3,)  # Вход для дополнительных параметров

# Инициализация ветвей сети
conv_branch = create_convolutional_branch(image_input_shape)
fc_branch = create_fully_connected_branch(sensor_input_shape)

# Входные слои
input_image = layers.Input(shape=image_input_shape)
input_sensors = layers.Input(shape=sensor_input_shape)

# Проход через ветви
conv_output = conv_branch(input_image)  # Выход конволюционной ветви
fc_output = fc_branch(input_sensors)  # Выход полносвязной ветви

# Объединение выходов
combined = layers.concatenate([conv_output, fc_output])

# Полносвязный слой для классификации
dense_output = layers.Dense(64, activation='relu')(combined)
final_output = layers.Dense(3, activation='softmax')(dense_output)  # Классификация на 3 класса

# Создаем модель
model = models.Model(inputs=[input_image, input_sensors], outputs=final_output)

# Компиляция модели
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Вывод информации о модели
model.summary()

# Пример генерации тестовых данных
num_samples = 1000
x_images = np.random.random((num_samples, 225, 225, 3))
x_sensors = np.random.random((num_samples, 3))
y = np.random.randint(0, 3, size=(num_samples,))

# Преобразование меток в one-hot формат
y = tf.keras.utils.to_categorical(y, num_classes=3)

# Обучение модели
model.fit([x_images, x_sensors], y, epochs=10, batch_size=32)

# Оценка модели
x_images_test = np.random.random((200, 225, 225, 3))
x_sensors_test = np.random.random((200, 3))
y_test = np.random.randint(0, 3, size=(200,))
y_test = tf.keras.utils.to_categorical(y_test, num_classes=3)

# Оценка модели
test_loss, test_accuracy = model.evaluate([x_images_test, x_sensors_test], y_test)
print(f'Test accuracy: {test_accuracy:.4f}')

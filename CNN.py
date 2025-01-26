import tensorflow as tf
from tensorflow.keras import layers, models

model = models.Sequential()

# Первый сверточный слой
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))

# Второй сверточный слой
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# Третий сверточный слой
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

# Полносвязный слой
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

# Компилируем модель
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
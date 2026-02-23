import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.regularizers import l2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization, InputLayer
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import seaborn as sns

def load_and_prepare_data(file_path, columns, selected_features):
    data = pd.read_csv(file_path, sep=" ", header=None)
    data.drop(columns=[26, 27], inplace=True)
    data.columns = columns
    data = data[['unit_number', 'time_in_cycles'] + selected_features]
    data['RUL'] = data['time_in_cycles'] / data.groupby('unit_number')['time_in_cycles'].transform('max')
    return data

def normalize_data(data_list, feature_cols):
    full_data = pd.concat(data_list, ignore_index=True)
    scaler = StandardScaler()
    scaler.fit(full_data[feature_cols])
    normalized_data = []
    for df in data_list:
        df_copy = df.copy()
        df_copy[feature_cols] = scaler.transform(df_copy[feature_cols])
        normalized_data.append(df_copy)
    return normalized_data, scaler

def augment_data(data, feature_cols, noise_level=0.01, augment_factor=1):
    augmented_dfs = [data]
    for i in range(augment_factor):
        noisy_data = data.copy()
        for feature in feature_cols:
            noise = np.random.normal(0, noise_level, size=len(noisy_data))
            noisy_data[feature] = noisy_data[feature] + noise
        augmented_dfs.append(noisy_data)
    return pd.concat(augmented_dfs, ignore_index=True)

columns = ['unit_number', 'time_in_cycles', 'setting_1', 'setting_2', 'TRA', 'T2', 'T24', 'T30', 'T50', 'P2', 'P15',
           'P30', 'Nf', 'Nc', 'epr', 'Ps30', 'phi', 'NRf', 'NRc', 'BPR', 'farB', 'htBleed', 'Nf_dmd', 'PCNfR_dmd',
           'W31', 'W32']
selected_features = ['T24', 'T30', 'T50', 'P15', 'P30', 'Nf', 'Nc', 'Ps30', 'phi', 'NRf', 'NRc', 'BPR', 'htBleed',
                     'W31', 'W32']

# Предварительная обработка
train_data = load_and_prepare_data("train_FD001.txt", columns, selected_features)
# Аугментация
train_data_augmented = augment_data(train_data, selected_features, noise_level=0.01, augment_factor=2)
# Разделение по unit_number
units = train_data_augmented['unit_number'].unique()
train_units, test_units = train_test_split(units, test_size=0.2, random_state=42)
# Обучающая и тестовая выборки по unit_number
train_df = train_data_augmented[train_data_augmented['unit_number'].isin(train_units)].reset_index(drop=True)
test_df = train_data_augmented[train_data_augmented['unit_number'].isin(test_units)].reset_index(drop=True)
# Обучаем scaler на обучающих данных
scaler = StandardScaler()
scaler.fit(train_df[selected_features])
# Нормализуем обучающие и тестовые данные
train_df_norm = train_df.copy()
train_df_norm[selected_features] = scaler.transform(train_df[selected_features])
test_df_norm = test_df.copy()
test_df_norm[selected_features] = scaler.transform(test_df[selected_features])

# Теперь разделяем на X и y для обучения модели
X_train = train_df_norm[selected_features]
y_train = train_df_norm['RUL']
X_test = test_df_norm[selected_features]
y_test = test_df_norm['RUL']

# Параметры последовательности
sequence_length = 20
def create_sequences(data, feature_cols, target_col, sequence_length):
    sequences = []
    targets = []
    for unit in data['unit_number'].unique():
        unit_data = data[data['unit_number'] == unit]
        features = unit_data[feature_cols].values
        target = unit_data[target_col].values
        for i in range(len(unit_data) - sequence_length):
            seq = features[i:i+sequence_length]
            label = target[i+sequence_length-1]  # RUL на конце последовательности
            sequences.append(seq)
            targets.append(label)
    return np.array(sequences), np.array(targets)

# Создаем обучающие последовательности
X_train_seq, y_train_seq = create_sequences(train_df_norm, selected_features, 'RUL', sequence_length)
# Создаем тестовые последовательности
X_test_seq, y_test_seq = create_sequences(test_df_norm, selected_features, 'RUL', sequence_length)

# Построение модели с несколькими слоями LSTM
model = Sequential()
# Первый LSTM слой с регуляризацией, BatchNormalization, Dropout
model.add(LSTM(128, activation='relu', return_sequences=True,
               kernel_regularizer=l2(0.001), input_shape=(sequence_length, len(selected_features))))
model.add(BatchNormalization())
model.add(Dropout(0.3))

# Второй LSTM слой
model.add(LSTM(64, activation='relu', return_sequences=False,
               kernel_regularizer=l2(0.001)))
model.add(BatchNormalization())
model.add(Dropout(0.3))

# Полносвязный слой для регрессии
model.add(Dense(1, activation='linear'))  # для регрессии

# Компиляция с указанием функции потерь, метрик
model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['mean_absolute_error'])

# Обучение с EarlyStopping и ReduceLROnPlateau для динамической настройки обучения
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5)

history = model.fit(
    X_train_seq, y_train_seq,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stop, reduce_lr]
)

# Предсказываем
predictions = model.predict(X_test_seq)

# Для оценки качества: MSE, MAE, R2 и визуализации

mse = mean_squared_error(y_test_seq, predictions)
mae = mean_absolute_error(y_test_seq, predictions)
r2 = r2_score(y_test_seq, predictions)

print(f"MSE: {mse:.3f}")
print(f"MAE: {mae:.3f}")
print(f"R2: {r2:.3f}")

# Визуализация
plt.figure(figsize=(10,6))
plt.plot(y_test_seq, label='Истинный RUL')
plt.plot(predictions.flatten(), label='Предсказанный RUL')
plt.legend()
plt.title('Сравнение истинных и предсказанных значений RUL')
plt.show()

# Условие для бинарной классификации (если, RUL < 50)
threshold = 50
y_true_bin = (y_test_seq < threshold).astype(int)
y_pred_prob = 1/(1 + np.exp(-predictions.flatten()))  # для модели с сигмоидом

fpr, tpr, thresholds = roc_curve(y_true_bin, y_pred_prob)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0,1], [0,1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC-кривая')
plt.legend(loc='lower right')
plt.show()

# Построим матрицу ошибок
y_pred_bin = (y_pred_prob >= 0.5).astype(int)
cm = confusion_matrix(y_true_bin, y_pred_bin)

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()



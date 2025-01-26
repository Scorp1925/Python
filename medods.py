import os
import base64
import bcrypt
import jwt
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['JWT_EXPIRATION'] = 15  # minutes
app.config['REFRESH_TOKEN_EXPIRATION'] = 7  # days

# Временное хранилище токенов для пользователей
tokens_storage = {}  # будет хранить пары access и refresh токенов


def generate_jwt(user_id, client_ip):
    payload = {
        'user_id': user_id,
        'ip': client_ip,
        'exp': datetime.utcnow() + timedelta(minutes=app.config['JWT_EXPIRATION'])
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='SHA512')


def generate_refresh_token():
    random_token = os.urandom(32)
    return base64.b64encode(random_token).decode('utf-8')


def hash_refresh_token(token):
    return bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt())


@app.route('/auth/tokens/<user_id>', methods=['POST'])
def get_tokens(user_id):
    client_ip = request.remote_addr

    # Генерация токенов
    access_token = generate_jwt(user_id, client_ip)
    refresh_token = generate_refresh_token()
    hashed_refresh_token = hash_refresh_token(refresh_token)

    # Сохранение токенов в хранилище
    tokens_storage[user_id] = {
        'access_token': access_token,
        'hashed_refresh_token': hashed_refresh_token,
        'client_ip': client_ip
    }

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    })


@app.route('/auth/refresh', methods=['POST'])
def refresh_token():
    user_id = request.json.get('user_id')
    refresh_token = request.json.get('refresh_token')
    current_ip = request.remote_addr

    stored_tokens = tokens_storage.get(user_id)

    if not stored_tokens:
        return jsonify({'message': 'Invalid user ID'}), 401

    # Проверка соответствия refresh токена
    if not bcrypt.checkpw(refresh_token.encode('utf-8'), stored_tokens['hashed_refresh_token']):
        return jsonify({'message': 'Invalid refresh token'}), 401

    # Проверка IP адреса
    if stored_tokens['client_ip'] != current_ip:
        # Отправка предупреждения по email (моковые данные)
        print(f"Warning email sent to user about IP address change. Current IP: {current_ip}")

    # Генерация нового access токена
    new_access_token = generate_jwt(user_id, current_ip)

    return jsonify({
        'access_token': new_access_token,
        'refresh_token': refresh_token  # Возвращаем тот же refresh токен
    })


if __name__ == '__main__':
    app.run(debug=True)

import socket
import pickle
import random
import rsa

HOST = 'localhost'
PORT = 9999

# Генерируем ключи клиента
public_key, private_key = rsa.newkeys(1024)

# Отправляем открытый ключ на сервер
with socket.socket() as sock:
    sock.connect((HOST, PORT))
    sock.send(pickle.dumps(public_key))

    # Принимаем открытый ключ сервера
    msg = sock.recv(1024)
    server_public_key = pickle.loads(msg)

    # Шифруем сообщение
    message = b"Secret message1"
    encrypted = rsa.encrypt(message, server_public_key)
    sock.send(encrypted)

    # Принимаем ответ от сервера
    encrypted_response = sock.recv(1024)
    response = rsa.decrypt(encrypted_response, private_key)
    print("Ответ:", response.decode())

import socket
import pickle
import rsa

HOST = 'localhost'
PORT = 9999

# Генерируем ключи сервера
public_key, private_key = rsa.newkeys(1024)

with socket.socket() as sock:
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()

    # Принимаем открытый ключ клиента
    msg = conn.recv(1024)
    client_public_key = pickle.loads(msg)

    # Отправляем открытый ключ сервера
    conn.send(pickle.dumps(public_key))
    # Принимаем зашифрованное сообщение
    encrypted_message = conn.recv(1024)
    message = rsa.decrypt(encrypted_message, private_key)
    print("Получено сообщение:", message.decode())

    # Отправляем ответ
    response = b"Hello client2"
    encrypted_response = rsa.encrypt(response, client_public_key)
    conn.send(encrypted_response)

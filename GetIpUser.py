import socket
import threading
import json

ip_storage = {}

def store_user_ip(user_id, ip_address, message_type):
    if user_id not in ip_storage:
        ip_storage[user_id] = {}
    ip_storage[user_id][message_type] = ip_address

def get_stored_ip(user_id, message_type):
    user_data = ip_storage.get(user_id, {})
    return user_data.get(message_type, "Bilgi bulunamadı.")

def client_handler(client_socket, address):
    user_data = client_socket.recv(1024).decode()
    user_info = json.loads(user_data)
    user_id = user_info["user_id"]
    user_ip = address[0]
    message_type = user_info["message_type"]
    store_user_ip(user_id, user_ip, message_type)
    print(f"{user_id} kullanıcısının {message_type} IP adresi {user_ip} olarak kaydedildi.")
    client_socket.close()

def main():
    server_ip = "0.0.0.0"  # Tüm ağ arayüzlerini dinle
    server_port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Dinleniyor... {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()

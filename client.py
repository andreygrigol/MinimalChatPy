import socket
import threading

def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                print("Desconectado do servidor.")
                client_socket.close()
                break
            print(message.decode())
    except Exception as e:
        print(f"Erro ao receber mensagem: {e}")
        client_socket.close()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8080))
    username = input("Digite seu nome de usuário: ")
    client_socket.send(username.encode())

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    try:
        while True:
            message = input().strip()
            if message.lower() == "sair":
                client_socket.close()
                break
            client_socket.send(f"{username}: {message}".encode())
    except Exception as e:
        print(f"Erro: {e}")
        client_socket.close()

if __name__ == "__main__":
    main()

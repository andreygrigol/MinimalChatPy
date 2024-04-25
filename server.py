import socket
import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 8080))
server_socket.listen()

sockets_list = [server_socket]
clients = {}

print("Servidor ativo. Aguardando usuários...")

def announce_message(sender_socket, message):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                if isinstance(message, str):
                    message = message.encode()
                client_socket.send(message)
            except Exception as e:
                print(f"Erro ao enviar mensagem para {clients[client_socket]} : {e}")
                client_socket.close()
                sockets_list.remove(client_socket)
                del clients[client_socket]

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = client_socket.recv(1024).decode()
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(f"Conexão estabelecida com {client_address[0]}:{client_address[1]} como {user}")
            announce_message(client_socket, f"{user} entrou no chat\n".encode())
        else:
            message = notified_socket.recv(1024)
            if message:
                user = clients[notified_socket]
                print(f"Mensagem recebida de {user}: {message.decode()}")
                announce_message(notified_socket, f"{user}:{message}".encode())
            else:
                user = clients[notified_socket]
                print(f"Conexão encerrada com {user}")
                announce_message(notified_socket, f"{user} deixou o chat\n".encode())
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                notified_socket.close()

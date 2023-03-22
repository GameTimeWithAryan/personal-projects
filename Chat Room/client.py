import socket
import threading
from sys import argv

from node import NetworkNode, MessageType, CONN_ERROR, INVALID_MSG_LEN_ERROR, WRONG_PASSWORD_MSG

HOST, PORT = socket.gethostbyname(socket.gethostname()), 5050
is_alive: bool = True


def authenticate_with_server(client_node: NetworkNode):
    global is_alive, argv
    while True:
        try:
            if len(argv) == 1:
                username = input("Enter your username - ")
            else:
                username = argv[1]
                argv = argv[:1]
                print(f"Enter your username - {username}")
            client_node.send_message(username, MessageType.NAME)
            if username != "admin":
                break

            password = input("Enter your password - ")
            client_node.send_message(password, MessageType.PASSWORD)

            _, response = client_node.recv_message()
            if response == WRONG_PASSWORD_MSG:
                print("Wrong password")
                continue
            print("Authenticated as admin successfully\n")
            break
        except socket.error as e:
            print(CONN_ERROR)
            is_alive = False


def send_messages_to_server(client_node: NetworkNode):
    global is_alive
    try:
        while is_alive:
            message = input()
            if message == "quit":
                is_alive = False
                break
            client_node.send_message(message, MessageType.MESSAGE)

    except socket.error:
        print(f"[SENDER] {CONN_ERROR}")
        return


def receive_messages_from_server(client_node: NetworkNode):
    received_message: str
    while is_alive:
        try:
            message_type, message = client_node.recv_message()
            match message_type:
                # Usually a join or a leave message of a client
                case MessageType.INFO.value:
                    received_message = f"[INFO] {message}"
                case MessageType.NAME.value:
                    sender_name = message
                    # if username of sender is received, chat message should follow
                    _, chat_message = client_node.recv_message()
                    received_message = f"{sender_name}: {chat_message}"
                case no_matches:
                    print(f"Received invalid message type {no_matches}")
                    continue
            print(received_message)

        except socket.error:
            print(CONN_ERROR)
            break
        except ValueError:
            print(INVALID_MSG_LEN_ERROR)


def run_client():
    """
    For communicating with the chat room server, allowing receiving and sending of messages
    at the same time, a thread of `receive_messages_from_server` function is created,
    while the `send_messages_to_server` function faclitates sending of messages to the server
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client_node = NetworkNode(client)

        authenticate_with_server(client_node)

        receiver_thread = threading.Thread(target=receive_messages_from_server, args=(client_node,))
        receiver_thread.start()

        send_messages_to_server(client_node)


if __name__ == "__main__":
    print("GWA's Chatroom")
    print("Type 'quit' to quit the program")
    print("Type and press enter to send message")
    print()
    run_client()

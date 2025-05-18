## Importing Modules
from concurrent.futures import ThreadPoolExecutor
from server import SocketServer
import socket
import signal
## ........


chats:list[SocketServer] = []
MAX_SERVERS = 5


def get_server_info() -> tuple:
    ## Configuring Host Details
    DEFAULT_HOSTNAME = "127.0.0.1"
    DEFAULT_HOSTPORT = 8080

    print("Enter Host Detail to run server : ")
    host_name = input(f"Host (default: {DEFAULT_HOSTNAME}) - ") or DEFAULT_HOSTNAME
    port = input(f"Port (default: {DEFAULT_HOSTPORT}) - ")
    try:
        host_port = int(port) if port else DEFAULT_HOSTPORT
        if host_port < 1 or host_port > 65535:
            raise ValueError
    except ValueError:
        print("Invalid port. Using default.")
        return None
    ## .........

    return (host_name, host_port)

def shutdown_all_servers(signum=None, frame=None):
    for chat in chats:
        print(f"Shutting down {chat.host_ip}:{chat.host_port} server")
        chat._shutdown()

def create_server():
    # Handling Ctrl+C
    signal.signal(signal.SIGINT, shutdown_all_servers)
    
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                if len(chats) >= MAX_SERVERS:
                    print(f"Max server limit ({MAX_SERVERS}) reached. Cannot create more.")
                    break

                info = get_server_info()
                if info is None:
                    continue

                try:
                    newChat = SocketServer(info)
                    newChat._startServer()
                    executor.submit(newChat.online)
                    chats.append(newChat)
                    print("Server started successfully.")

                except socket.error as err:
                    print(f"Failed to start server: {err}")

                choice = input("Do you want to create a new chat server [y/n] : ")
                if choice.lower() == 'shutdown':
                    shutdown_all_servers()
                    break
                elif choice.lower() != 'y':
                    print("Server Manager shutting down.")
                    break
                    
    except KeyboardInterrupt:
        print("\n[!] Keyboard Interrupt. Shutting down all servers .....")

    finally:
        for chat in chats:
            try:
                chat._shutdown()
            except:
                pass


if __name__ == "__main__":
    create_server()
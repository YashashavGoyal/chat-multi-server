## Importing Modules
from concurrent.futures import ThreadPoolExecutor
from server import SocketServer
import socket
import signal
## ........


chats:list[SocketServer] = []
MAX_SERVERS = 5

## Gather Server Address
def get_server_info() -> tuple[str, int]:
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

        if any(chat.host_port == host_port for chat in chats):
            print(f"Server already running on port {host_port}. Auto picking different port")
            used_ports = {chat.host_port for chat in chats}
            host_port = DEFAULT_HOSTPORT
            while host_port in used_ports:
                host_port += 1

        return (host_name, host_port)

    except ValueError:
        print("Invalid port. Using default.")
        return None
    ## .........
## ......

## Shutting Servers Down
def shutdown_all_servers(signum=None, frame=None):
    print("\n[!] Shutting down all servers...")
    for chat in chats:
        try:
            print(f"Shutting down {chat.host_ip}:{chat.host_port}")
            chat._shutdown()
        except Exception as e:
            print(f"Error shutting down {chat.host_ip}:{chat.host_port}: {e}")
## ......

## Start New Chat
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
## ......

## Starting Menu
def show_banner():
    print("="*40)
    print(" 🖥️  Multi-Chat Server Manager")
    print(" Press Ctrl+C or type 'shutdown' to exit.")
    print("="*40)
## ......


if __name__ == "__main__":
    show_banner()
    create_server()
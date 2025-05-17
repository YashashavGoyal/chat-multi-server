from threading import Thread
import socket
import sys


## Configuring Host Details
def get_hosts_info():
    while True:
        try:
            print("Enter Server Details : ")
            host_ip = input("Server Ip : ")
            host_port = int(input("Server Port : "))
            if host_port < 1: 
                raise ValueError
            return (host_ip, host_port)
        except ValueError:
            print("Port number should be an Positive Integer")
## .........


## Function For Receiving Messages
def recv_msg(soc:socket.socket):
    while True:
        try:
            msg = soc.recv(1024).decode()
            if not msg or msg.lower() in ("exit", "q"):
                print("Server closed")
                soc.close()
                break
            sys.stdout.write('\r' + ' ' * 80 + '\r')  # clear current input line
            print(f"Server : {msg}")
            sys.stdout.write("You : ")
            sys.stdout.flush()
        except:
            print("connection lost")
## ..........


def connect_server():
    try:
        # Create Socket
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host_info = get_hosts_info()
        soc.connect(host_info)

        ## Start Receving Thread
        Thread(target=recv_msg, args=(soc,), daemon=True).start()

        ## ..........

        ## Sending Msg -- Main Thread
        while True:
            send_msg = input("You : ")
            if send_msg.lower() in ("exit", "q"):
                soc.send(send_msg.encode())
                soc.close()
                print("You closed the connection")
                exit(0)
            elif send_msg:
                soc.send(send_msg.encode())
        ## ..........

    except socket.error as e:
        print(f"Could not connect to server: {e}")

    except KeyboardInterrupt:
        try:
            soc.close()
        except:
            pass
        print("\nClient terminated by user.")

    finally:
        sys.exit()

if __name__ == "__main__":
    connect_server()
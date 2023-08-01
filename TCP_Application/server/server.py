import socket 
import threading
import os

BUFFER_SIZE = 64
PORT = 20941
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
MENU = r"""list of options:
    get files - get|filename
    upload files - put|filename
    list files - ls / dir
    help - show this message
"""

def transfer(conn, path):
    path = path.split('|')[-1].split("/")[-1]

    if os.path.exists(path):
        with open(path, "rb") as f:
            packet = f.read(BUFFER_SIZE)
            while len(packet) > 0:
                print(f"Getting {len(packet)} bytes")
                conn.send(packet)
                packet = f.read(BUFFER_SIZE)
            conn.send('DONE'.encode())
    else:
        conn.send('File not found'.encode())


def upload(conn, path):
    path = path.split('|')[-1].split("/")[-1]
    print(f"{path=}")
    with open(path, "wb") as f:
        while True:
            bits = conn.recv(BUFFER_SIZE)
            if bits.endswith('DONE'.encode()):
                print(f"Putting {len(bits)} bytes")
                f.write(bits[:-4])
                f.close()
                break
            f.write(bits)

def delete_file(path):
    try:
        os.remove(path)
        print(f"Deleted file {path}")
    except OSError as e:
        print("Error deleting file")

def client(conn, addr):
    try:
        print(f"NEW CONNECTION {addr} connected.")

        while True:
            msg = conn.recv(BUFFER_SIZE).decode()
            if msg:
                if msg == DISCONNECT_MESSAGE:
                    break

                elif msg.startswith("get|"):
                    transfer(conn, msg)
                
                elif msg.startswith("put|"):
                    print("Start uploading..")
                    upload(conn, msg)

                elif msg.startswith("rm|"):
                    delete_file(msg.split("|")[-1])


                elif msg == "dir" or msg == "ls":
                    list_dir = ' \n'.join(os.listdir()).encode()
                    print(f"send list dir {list_dir}")

                    for i in range(0, len(list_dir), BUFFER_SIZE):
                        print(i)
                        conn.send(list_dir[i:i+BUFFER_SIZE])
                
                else:
                    # print(f"[{addr}] {msg}")
                    for i in range(0, len(MENU.encode()), BUFFER_SIZE):
                        print(i)
                        conn.send(MENU.encode()[i:i + BUFFER_SIZE])

        conn.close()
    except KeyboardInterrupt:
        conn.send(DISCONNECT_MESSAGE.encode())
    
    except Exception as e:
        print("Error occur", e)

    finally:
        conn.close()
      

def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)

        print(" server is starting...")
        server.listen(5)
        print(f" Server is listening on {SERVER}")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=client, args=(conn, addr))
            thread.start()
            print(f"ACTIVE CONNECTIONS - {threading.active_count() - 1}")
    
    except KeyboardInterrupt:
        print("Closing server")
    
    except Exception as e:
        print("Error occur", e)
    
    finally:
        server.close()


if __name__ == "__main__":
    main()





import socket
import os

BUFFER_SIZE = 64
PORT = 20941
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)




def transfer(filename):
    client.send(filename.encode())
    path = filename.split("|")[-1]

    with open(os.getcwd() + "/" + path, "wb") as f:
        
        while True:
            bits = client.recv(BUFFER_SIZE)
            print(f"reading {len(bits)} size of bytes")
            
            if bits.endswith('DONE'.encode()):
                f.write(bits[:-4])
                f.close()
                print("Transfer completed")
                f.close()
                break
        
            if 'File not found'.encode() in bits:
                print ("Unable to find out the file")
                f.close()
                os.remove(os.getcwd() + "/" + path)
                break

            f.write(bits)


def upload(command):
    client.send(command.encode())
    path = command.split("|")[-1]
    print(path)

    if os.path.exists(path):
        with open(path, "rb") as f:
            packet = f.read(BUFFER_SIZE)
        
            while len(packet) > 0:
                print(f"reading {len(packet)} size of bytes")
                client.send(packet)
                packet = f.read(BUFFER_SIZE)
        
            client.send('DONE'.encode())
            f.close()
    
    else:
        client.send('File not found'.encode())


def send(msg):
    message = msg.encode()
    client.send(message)
    data = b""

    while True:
        chunck = client.recv(BUFFER_SIZE)
        print(len(chunck))

        if not chunck:
            break
        data += chunck
        print(data)

    print(data.decode())


def main():
    try:
        while True:
            msg = input("> ")

            if msg.startswith("get|"):
                transfer(msg)
            
            elif msg.startswith("put|"):
                upload(msg)
            
            else:
                send(msg)
    
    except KeyboardInterrupt:
        send(DISCONNECT_MESSAGE)
    
    except Exception as e:
        print("Error occur", e)
    
    finally:
        client.close()

if __name__ == "__main__":
    main()




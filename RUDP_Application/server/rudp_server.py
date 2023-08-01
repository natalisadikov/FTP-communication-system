import socket
import hashlib

IP_ADDR = "127.0.0.1"
PORT = 20941
BUFFER_SIZE = 64

def calc_checksum(data):
    return hashlib.md5(data).digest()

def ftp_server():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (IP_ADDR, PORT)
    print('Starting FTP server')
    sock.bind(server_address)

    while True:
        print(f"Server is listning on {IP_ADDR}")
        data, client_address = sock.recvfrom(BUFFER_SIZE)
        file_name = data.decode()
        print(f"Got request for {file_name}")

        try:
            with open(file_name, 'rb') as f:
                print(f"Sending {file_name} to {client_address}")
                while True:
                    data = f.read(BUFFER_SIZE)
                    if not data:
                        break
                    checksum = calc_checksum(data)
                    print(checksum)
                    sock.sendto(checksum + data, client_address)
                    print("Finish sending")
        except FileNotFoundError:
            print(f"{file_name} not found.")
            sock.sendto(b"Error: file not found.", client_address)

if __name__ == '__main__':
    ftp_server()

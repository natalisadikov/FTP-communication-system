import socket
import hashlib

IP_ADDR = "127.0.0.1"
PORT = 20941
BUFFER_SIZE = 64

def calc_checksum(data):
    return hashlib.md5(data).digest()

def udp_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    file_name = input("Enter file name to download: ")
    server_address = (IP_ADDR, PORT)
    print(f"Send request for {file_name}")
    sock.sendto(file_name.encode(), server_address)

    try:
        with open(f'{file_name}', 'wb') as f:
            while True:
                data, server_address = sock.recvfrom(1056)
                checksum = data[:16]
                print(checksum)
                data = data[16:]
                print("Download complete")
                if not data:
                    break
                if checksum == calc_checksum(data):
                    f.write(data)
                else:
                    print("Checksum problem")

    except Exception as e:
        print("Can't download file:", e)

if __name__ == '__main__':
    udp_client()

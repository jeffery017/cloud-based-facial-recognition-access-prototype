import socket

def get_local_ip():
    # Create a socket and connect to an external address to determine the local IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # Google's public DNS server
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

print("Local IP Address:", get_local_ip())

if __name__ == "__main__":
    print(get_local_ip())
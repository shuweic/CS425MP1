import socket
import threading

lock = threading.Lock()
total_matches = 0

def send_query_to_server(server_ip, server_port, query):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    try:
        client.connect((server_ip, server_port))
        client.send(query.encode('utf-8'))

        response = ""
        while True:
            chunk = client.recv(32768).decode('utf-8')
            if "EOF" in chunk:
                response += chunk.replace("EOF", "")
                break
            response += chunk

        print(f"\nResults from {server_ip}:{server_port}:\n{response}")

        matches_part = [line for line in response.split('\n') if line.startswith('TOTAL_MATCHES:')]
        if matches_part:
            total_matches = int(matches_part[0].split(':')[1].strip())
            return total_matches

        return 0
    except Exception as e:
        print(f"Error connecting to {server_ip}:{server_port}: {e}")
        return 0
    finally:
        client.close()

def query_server(ip, port, query):
    global total_matches
    matches = send_query_to_server(ip, port, query)
    with lock:
        total_matches += matches

def main():
    servers = [
        ('172.22.95.32', 9999),
        ('172.22.157.33', 9999),
        ('172.22.159.33', 9999),
        ('172.22.95.33', 9999),
        ('172.22.157.34', 9999),
        ('172.22.159.34', 9999),
        ('172.22.95.34', 9999),
        ('172.22.157.35', 9999),
        ('172.22.159.35', 9999),
        ('172.22.95.35', 9999),
        # ('192.168.10.12', 9999)
    ]

    try:
        while True:
            query = input("Enter search pattern (or type 'exit' to disconnect): ")
            if query.lower() == 'exit':
                print("Disconnecting from all servers...")
                break

            global total_matches
            total_matches = 0

            threads = []
            for server_ip, server_port in servers:
                thread = threading.Thread(target=query_server, args=(server_ip, server_port, query))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            print(f"\nTotal matches across all servers: {total_matches}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

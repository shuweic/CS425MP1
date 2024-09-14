import socket
import threading

def send_query_to_server(server_ip, server_port, query, total_matches, lock):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

        # 打印服务器的日志查询结果
        print(f"\nServer {server_ip}:{server_port} response:\n{response}")

        # 查找和提取 TOTAL_MATCHES 信息
        match = re.search(r'TOTAL_MATCHES:(\d+)', response)
        if match:
            server_total_matches = int(match.group(1))
            # 使用锁来保证线程安全地修改 total_matches
            with lock:
                total_matches[0] += server_total_matches

    except Exception as e:
        print(f"Error connecting to {server_ip}:{server_port}: {e}")
    finally:
        client.close()

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
        ('172.22.95.35', 9999)
    ]

    try:
        while True:
            query = input("Enter search pattern (or type 'exit' to disconnect): ")
            if query.lower() == 'exit':
                print("Disconnecting from all servers...")
                break

            # total_matches 用列表来存储，因为列表是可变对象，可以在多线程中共享
            total_matches = [0]
            lock = threading.Lock()
            threads = []
            for server_ip, server_port in servers:
                thread = threading.Thread(target=send_query_to_server, args=(server_ip, server_port, query, total_matches, lock))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            # 所有线程执行完后输出总的匹配数
            print(f"\nTotal matches across all servers: {total_matches[0]}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

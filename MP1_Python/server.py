import socket
import subprocess
import re
import os

def execute_grep_on_logs(query):
    
    log_files = [f for f in os.listdir() if f.endswith('.log')]
    result = ""
    total_matches = 0

    for log_file in log_files:
        command = ['grep', '-E', '-n', query, log_file]
        try:
            grep_result = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            matches = grep_result.strip().split('\n')

            if matches:
                result += f"\nFile: {log_file}\n"
                for match in matches:
                    result += f"Line {match.split(':')[0]}: {match.split(':', 1)[1]}\n"
                total_matches += len(matches)
            else:
                result += f"File: {log_file}\nNo matches found\n"

        except subprocess.CalledProcessError:
            result += f"File: {log_file}\nNo matches found\n"

    result += f"\n"
    return result, total_matches

def handle_client(client_socket):
    try:
        while True:
            query = client_socket.recv(1024).decode('utf-8')
            if not query or query.lower() == 'exit':
                print("Client requested disconnection or sent empty query.")
                break
            
            print(f"Received query: {query}")
            
            result, total_matches = execute_grep_on_logs(query)
            
            client_socket.send(result.encode('utf-8'))
            
            client_socket.send(b"EOF")

            client_socket.send(f"TOTAL_MATCHES:{total_matches}".encode('utf-8'))
            break
    finally:
        client_socket.close()
        print("Connection closed with the client.")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()

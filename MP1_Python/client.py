import socket
import threading
import argparse
import time

# Lock for synchronizing access to shared resources between threads
lock = threading.Lock()
# Variable to keep track of total matches across all servers
total_matches = 0
# Dictionary to store the number of matches per server
server_matches = {}

def send_query_to_server(server_ip, server_port, query):
    """
    Sends a query to a specified server and returns the number of matches found.
    
    Args:
        server_ip (str): IP address of the server.
        server_port (int): Port number of the server.
        query (str): Search query to send to the server.
        
    Returns:
        int: Number of matches found by the server.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    try:
        # Connect to the server
        client.connect((server_ip, server_port))
        # Send the query
        client.send(query.encode('utf-8'))

        # Receive the response from the server
        response = ""
        while True:
            chunk = client.recv(32768).decode('utf-8')
            if "EOF" in chunk:
                response += chunk.replace("EOF", "")
                break
            response += chunk

        print(f"\nResults from {server_ip}:{server_port}:\n{response}")

        # Extract file name from response
        file_name = [line for line in response.split('\n') if line.startswith('File:')]
        if file_name:
            name = file_name[0].split(':')[1].strip()
        
        # Extract total matches from response
        matches_part = [line for line in response.split('\n') if line.startswith('TOTAL_MATCHES:')]
        if matches_part:
            total_matches = int(matches_part[0].split(':')[1].strip())
            server_matches[name] = total_matches
            return total_matches

        return 0
    except Exception as e:
        print(f"Error connecting to {server_ip}:{server_port}: {e}")
        return 0
    finally:
        client.close()

def query_server(ip, port, query):
    """
    Queries a server and updates the global total matches variable.
    
    Args:
        ip (str): IP address of the server.
        port (int): Port number of the server.
        query (str): Search query to send to the server.
    """
    global total_matches
    matches = send_query_to_server(ip, port, query)
    with lock:
        total_matches += matches

def main():
    """
    Main function to handle user input, create threads for querying servers, 
    and print results.
    """
    # List of servers to query
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
        
        # ('192.168.10.12', 9999),
        # ('10.193.255.134', 9999)
    ]

    try:
        while True:
            query = input("Enter search pattern (or type 'exit' to disconnect): ")
            if query.lower() == 'exit':
                print("Disconnecting from all servers...")
                break

            global total_matches
            total_matches = 0
            server_matches.clear()

            # Record the start time
            start_time = time.time()

            # Create and start a thread for each server
            threads = []
            for server_ip, server_port in servers:
                thread = threading.Thread(target=query_server, args=(server_ip, server_port, query))
                threads.append(thread)
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            # Record the end time
            end_time = time.time()
            # Calculate latency in milliseconds
            latency = (end_time - start_time) * 1000

            # Print the results
            for name, matches in server_matches.items():
                print(f"\nFile: {name}: {matches} matches")

            print(f"Total matches across all servers: {total_matches}")
            print(f"Total latency: {latency}ms\n")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

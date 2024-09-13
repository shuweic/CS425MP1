package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"sync"
)

var servers = []struct {
	IP   string
	Port int
}{
	{"10.195.125.150", 9000},
	// {"172.22.95.32", 9000},
	// {"172.22.157.33", 9000},
	// {"172.22.159.33", 9000},
	// {"172.22.95.33", 9000},
	// {"172.22.157.34", 9000},
	// {"172.22.159.34", 9000},
	// {"172.22.95.34", 9000},
	// {"172.22.157.35", 9000},
	// {"172.22.159.35", 9000},
	// {"172.22.95.35", 9000},
}

// Function to query a single server and return the result
func queryServer(ip string, port int, query string, wg *sync.WaitGroup, results chan<- string) {
	defer wg.Done()

	// Connect to the server
	address := fmt.Sprintf("%s:%d", ip, port)
	conn, err := net.Dial("tcp", address)
	if err != nil {
		results <- fmt.Sprintf("Error connecting to %s: %v", address, err)
		return
	}
	defer conn.Close()

	// Send the query to the server
	_, err = fmt.Fprintf(conn, query)
	if err != nil {
		results <- fmt.Sprintf("Error sending query to %s: %v", address, err)
		return
	}

	// Read the full response from the server
	reader := bufio.NewReader(conn)
	var serverResult string
	lineCnt := 0
	for {
		response, err := reader.ReadString('\n')
		if err != nil {
			if err.Error() == "EOF" {
				break
			}
			results <- fmt.Sprintf("Error reading from %s: %v", address, err)
			return
		}

		// Accumulate the response and count lines
		serverResult += response
		lineCnt++
	}

	// Send the result back with server details
	results <- fmt.Sprintf("Server: %s\n%s\nTotal lines received: %d\n", address, serverResult, lineCnt)
}

func main() {
	// Get the query from the user
	scanner := bufio.NewScanner(os.Stdin)
	fmt.Print("Enter the text to query: ")
	scanner.Scan()
	query := scanner.Text()

	// Channel to collect results from all servers
	results := make(chan string, len(servers))
	var wg sync.WaitGroup

	// Query all servers in parallel
	for _, server := range servers {
		wg.Add(1)
		go queryServer(server.IP, server.Port, query, &wg, results)
	}

	// Wait for all goroutines to finish
	wg.Wait()
	close(results)

	// Print results from all servers
	for result := range results {
		fmt.Println(result)
	}
}

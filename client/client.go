package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	// Connect to the server
	conn, err := net.Dial("tcp", "10.195.125.150:9000") // Replace with the worker's IP
	if err != nil {
		fmt.Println("Error connecting to server:", err)
		os.Exit(1)
	}
	defer conn.Close()

	// Get the query from the user
	scanner := bufio.NewScanner(os.Stdin)
	fmt.Print("Enter the text to query: ")
	scanner.Scan()
	query := scanner.Text()

	// Send the query to the server
	_, err = fmt.Fprintf(conn, query)
	if err != nil {
		fmt.Println("Error sending query to server:", err)
		os.Exit(1)
	}

	// Read the full response from the server in chunks
	reader := bufio.NewReader(conn)
	lineCnt := 0
	for {
		// Read until we reach the end of the data (EOF)
		response, err := reader.ReadString('\n') // Read until newline, or you can use a specific delimiter
		if err != nil {
			if err.Error() == "EOF" {
				break // End of data
			}
			fmt.Println("Error reading from server:", err)
			os.Exit(1)
		}

		// Print each chunk of data as it's received
		fmt.Print(response)
		lineCnt++
	}
	fmt.Println("\nTotal lines received:", lineCnt)
}

package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
)

func handleConnection(conn net.Conn) {
	defer conn.Close()

	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	if err != nil {
		log.Println(err)
		return
	}

	query := string(buf[:n])
	fmt.Println("Received query: ", query)

	// Check if the log file exists
	if _, err := os.Stat("machine.1.log"); os.IsNotExist(err) {
		log.Println("Log file does not exist!")
		conn.Write([]byte("Log file not found"))
		return
	}

	// Run grep on the log file (assuming "machine.1.log" as the file name)
	cmd := exec.Command("grep", query, "machine.1.log")
	output, err := cmd.CombinedOutput()

	// Handle case when no matches are found
	if err != nil && string(output) == "" {
		log.Println("No matches found for query.")
		conn.Write([]byte("No matches found."))
		return
	} else if err != nil {
		log.Println("Error running grep:", err)
		conn.Write([]byte("Error running grep"))
		return
	}

	// Send the grep output back to the client
	conn.Write(output)
}

func main() {
	listener, err := net.Listen("tcp", ":9000") // Listen on port 9000
	if err != nil {
		log.Fatal(err)
	}
	defer listener.Close()

	fmt.Println("Worker listening on port 9000...")
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Println(err)
			continue
		}
		go handleConnection(conn)
	}
}

package main

import (
	"log"
	"os"
	"time"
)

func main() {
	f, err := os.Create("machine.1.log")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	logger := log.New(f, "INFO: ", log.LstdFlags)
	for i := 0; i < 300000; i++ {
		logger.Println("This is a sample log entry number", i)
		time.Sleep(1 * time.Millisecond)
	}
}

# CS425 G87 MP1

## Overview

This project implements a basic client-server architecture for querying log files in a distributed system. The server listens for incoming requests from clients, processes the queries, and returns the relevant log entries.


## Structure

```bash
project_root/
├── cs425_g87/
└── xxx.log   <-- Log file go here
```

## Prepare

    In client.py, update the servers variable with the correct IP addresses and port numbers under the section labeled '# List of servers to query'.

## How to run

```bash
    python cs425_g87/MP1_Python/server.py
```
```bash
    python cs425_g87/MP1_Python/client.py
```

## Unit test

```bash
    python cs425_g87/MP1_Python/test.py
```
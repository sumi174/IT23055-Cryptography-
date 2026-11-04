# OSI Layer Simulation – Live Project

## Project Overview
This project demonstrates the working process of the **7 layers of the OSI (Open Systems Interconnection) Model** through a client-server communication system using C socket programming and Python visualization.

The project shows how data is encapsulated at the sender side and decapsulated at the receiver side.

## Features
- Simulation of all 7 OSI layers.
- Client-server communication using TCP sockets.
- Implemented using C programming and Winsock.
- Python-based terminal visualization.
- Step-by-step encapsulation and decapsulation process.
- Progress display after every two OSI layers.
- Server acknowledgment after successful message transmission.

## Technologies Used
- C Programming
- Python
- TCP Socket Programming
- Winsock2
- GCC Compiler

## Project Structure

OSI-Communication-Simulation/
│
├── .gitignore
├── README.md
│
├── .vscode/
│   └── c_cpp_properties.json
│
├── python/
│   └── visualizer.py
│
└── src/
    ├── client.c
    ├── server.c
    ├── layers.c
    └── layers.h

## Requirements
- Windows 10 or Windows 11
- GCC Compiler (MinGW)
- Python 3
- Visual Studio Code (recommended)

## How to Compile

Open a terminal in the project folder and run:

gcc -Wall -Wextra -mconsole -o server.exe src/server.c src/layers.c -lws2_32

gcc -Wall -Wextra -mconsole -o client.exe src/client.c src/layers.c -lws2_32

## How to Run

**Step 1: Start the Server**

Open a terminal and run:

.\server.exe

**Step 2: Run the Python Visualizer**

Open another terminal in the same project folder and run:

python python/visualizer.py

**Step 3: Observe the Simulation**

Enter a message when prompted. The visualizer will show the OSI layer encapsulation and decapsulation process, along with the server acknowledgment.

## Working Process

1. The sender starts with the Application Layer (Layer 7).
2. Data moves downward through the OSI layers.
3. The client sends the simulated packet to the server using TCP sockets.
4. The server receives the message and sends an acknowledgment.
5. The receiver demonstrates decapsulation from Layer 1 to Layer 7.

## Note
This is an educational simulation of the OSI model. The layer headers are simulated for demonstration purposes and do not represent actual network protocol headers at every OSI layer.



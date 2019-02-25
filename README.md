# Orange Tree
## About

Orange Tree is a Python-based software complex, primary purpose of which is to connect multiple Orange PI microcomputers in a single ecosystem and provide debugging/configuration for their GPIO pins, thus turning the complex into highly-flexible base for a range of IoT solutions.  
Complex is separated in 2 parts:
- *Server*. Serves as a hub, allowing users to monitor, modify, debug and configure the system.  
Technology stack: Flask (Flask + Flask-Security + Flask-SQLAlchemy + Flask-SocketIO), SQLAlchemy, sockets, pycryptodome.
- *Client*. Headless application, that is run on a target Orange PI PC, which connects to the server and may be used for pin configuration.  
Technology stack: WiringPI-Python-OP, sockets, psutil, sockets, pycryptodome.  
  
## Installing

### Prerequisites

- Server
  - Python (3.7+) interpreter.
  - MySQL/MariaDB server (in case you want to use it instead of SQLite3)
- Client
  - Armbian OS
  - Python (3.7+) interpreter.

### Server

- Clone/Download the source
- Navigate to project directory and run the installer by calling  
```bash
python3 server_setup.py install
```
*NOTE*: There are known occasions when setuptools fails to install several dependencies. So in case you'll run into any errors, simply re-run the installer - second time it usually gets it right.

### Client

- Clone/Download and install the [WiringPI-Python-OP](https://github.com/lanefu/WiringPi-Python-OP) library. Follow the instructions in that repo's readme file.
- Clone/Download the source
- Navigate to project directory and run the installer by calling
```bash
python3 client_setup.py install
```

## Running

### Server

- Go to **server** sub-folder, open **config.py** and configure the application.
- Once done - go back to root folder and run the application
```bash
python3 run_server.py
```

### Client

- Go to **client** sub-folder, open **config.py** and configure the application. **Make sure encryption key and IV matches the one used by server, otherwise it won't be able to communicate with it** .
- Once done - go back to root folder and run the application
```bash
python3 run_client.py
```
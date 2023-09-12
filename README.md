# Orion RSH Server

- In development
- Python remote command execution server

# Do not use for corporate environments

- Still needs to be tested for possible vulnerabilities
- Does not have a custom config file with configurations

# Main issue(s)

- There will be future updates on shell features

# Usage

- You will need a TCP client to connect to the server with port specification like:
  `nc localhost 8080`

- You must run `server.py` as root or with sudo permissions as it gets hashes from /etc/shadow (it uses setuid after authentication, root access is not given by default)
- After server is running, have your client connect to the same port

# Preview

![preview](https://raw.githubusercontent.com/shuban-789/Markdown-images/main/Screenshot%202023-09-09%20142952.png)

# Diagram

![diagram](https://raw.githubusercontent.com/shuban-789/Markdown-images/main/image%20(3).png)

# Coming soon!

- Customizable configurations

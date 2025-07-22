# Notice (7/22/2025)

- This repository will be archived. This project, although simple, was the beginning of my experience through real hands-on project based learning experience. Further changes are unlikely, but this repository is available for fork.

# Orion RSH Server

- Python remote command execution server

# Do Not Use for Corporate Environments

- Still needs to be tested for possible vulnerabilities
- Does not have a custom config file with configurations (Although this is in store for update 2.3)
- Each update newer supported configs will be added. Each config, its functions, and its options can be read in the documentation

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

- To be determined
- Most likely more customizable configurations and shell features
- Use local PAM policies

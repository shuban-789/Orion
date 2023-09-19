

1 of 5,331
(no subject)
Inbox

Shuban Pal <cybergeek11929@gmail.com>
Attachments
9:41 AM (3 minutes ago)
to Shuban


 One attachment
  •  Scanned by Gmail
######################################################
# Authors: Shuban Pal and Hayden Chen
# Application: Orion RSH Server
# Version: 2.3
# Documentation: https://github.com/shuban-789/Orion
######################################################

import crypt
import os
import pwd
import socket
import spwd
import ssl
import subprocess
import threading
import time

### Global Configs ###

ALLOWROOT="yes"
BANNEDUSERS=[]
SSLCERT=""
SSLKEY=""

### CONFIG COLLECTION: ORION V2.3 ###

### PARSING ALGORITHM: ORION V2.3 ###
o = open("/etc/orion/orion.conf","r")
configs = o.readlines()
for i in configs:
	n = i.strip()
	if "AllowRoot=" in n:
		if n[10:] == "yes":
			ALLOWROOT="yes"
		elif n[10:] == "no":
			ALLOWROOT="no"
		else:
			ALLOWROOT="yes"
	if "BannedUsers=" in n:
		li = n[12:]
		banlist = li.split(",")
		for j in banlist:
			BANNEDUSERS.append(j)
	if "SSLcert=" in n:
		SSLCERT = n[8:]
	if "SSLkey=" in n:
		SSLKEY = n[7:]

### END OF CONFIG PARSING: ORION V2.3

def read_shell_output(shell_process, client_socket, stop_flag):
    for line in shell_process.stdout:
        if stop_flag.is_set():
            break
        client_socket.send(line)

def get_uid(username):
    try:
        user_info = pwd.getpwnam(username)
        return user_info.pw_uid
    except KeyError:
        return None

def shell(client_socket):
    client_socket.send(b"Shell access granted. Type 'exit' to exit the shell.\n")
    shell_process = subprocess.Popen(['/bin/bash'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stop_flag = threading.Event()
    output_thread = threading.Thread(target=read_shell_output, args=(shell_process, client_socket, stop_flag))
    output_thread.start()

    while True:
        prompt = f"\033[96m[orionshell]>>> "
        prompt = prompt.encode('ASCII')
        time.sleep(0.2)
        client_socket.send(prompt)
        command = client_socket.recv(1024).decode("utf-8")
        if command.lower() == "exit":
            stop_flag.set() 
            break
        shell_process.stdin.write((command).encode("utf-8") + b'\n')
        shell_process.stdin.flush()

    shell_process.stdin.close()
    shell_process.stdout.close()
    shell_process.stderr.close()
    shell_process.kill()
    output_thread.join()
    client_socket.send(b"Shell session closed.\n")

def authenticate(client_socket, client_address):
    client_socket.send(b"Enter the username: ")
    username = client_socket.recv(1024).strip().decode("utf-8")
    if ALLOWROOT == "no" and username == "root":
       client_socket.send(b"Root access is not permitted on this system.\n")
       return False
    if len(BANNEDUSERS) != 0:
       for i in BANNEDUSERS:
          if username == i:
             return False
    try:
        PASSWORD = spwd.getspnam(username)
    except KeyError:
        client_socket.send(b"User not found.\n")
        return False

    client_socket.send(b"Enter the password: ")
    password_attempt = client_socket.recv(1024).strip().decode("utf-8")

    if crypt.crypt(password_attempt, PASSWORD.sp_pwdp) == PASSWORD.sp_pwdp:
        uid = get_uid(username)
        f = open("/var/log/orionrexec.log", "a")
        f.write(os.popen('date').read().strip() + f" ~ Successful login by user: {username} IP: {client_address}\n")
        f.close()
        os.setuid(uid)
        return True
    else:
        f = open("/var/log/orionrexec.log", "a")
        f.write(os.popen('date').read().strip() + f" ~ Unsuccessful login from IP: {client_address}\n")
        f.close()
        client_socket.send(b"Authentication failed.\n")
        return False

def main():
    server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server_context.load_cert_chain(SSLCERT, SSLKEY)
    s = server_context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    s.bind(('0.0.0.0', 8080))
    s.listen(1)

    print("Waiting for connection...")

    connection, address = s.accept()

    if authenticate(connection, address[0]):
        print("Authentication successful by: " + address[0])
        connection.send(b"Authentication successful. You now have access to the shell.\n")
        shell(connection)
    else:
        print("Authentication failed. Closing connection.")
        connection.close()

if __name__ == "__main__":
    main()

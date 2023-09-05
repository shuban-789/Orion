import socket
import os
import crypt
import spwd
import getpass
import sys

def hash_password(passw):
    return crypt.crypt(passw)

def shell(client_socket):
    client_socket.send(b"Shell access granted. Type 'exit' to exit the shell.\n")
    shell_process = subprocess.Popen(['/bin/bash'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        command = client_socket.recv(1024).decode("utf-8")
        if command.lower() == "exit":
            break
        shell_process.stdin.write(command.encode("utf-8") + b'\n')
        shell_process.stdin.flush()
        output = shell_process.stdout.readline().decode("utf-8")
        client_socket.send(output.encode("utf-8"))
    shell_process.stdin.close()
    shell_process.stdout.close()
    shell_process.stderr.close()
    shell_process.kill()
    client_socket.send(b"Shell session closed.\n")
    
def authenticate(client_socket, client_address):
    client_socket.send(b"Enter the username: ")
    username = client_socket.recv(1024).strip().decode("utf-8")
    
    try:
        PASSWORD = spwd.getspnam(username).sp_pwdp
    except KeyError:
        client_socket.send(b"User not found.\n")
        return False

    client_socket.send(b"Enter the password: ")
    password_attempt = client_socket.recv(1024).strip().decode("utf-8")

    if hash_password(password_attempt) == PASSWORD:
        f = open("/var/log/orionrexec.log","a")
        f.write(os.popen('date').read().strip() + " ~ Successful login by user: " + username + " IP: {client_address}\n")
        f.close()
        return True
    else:
        client_socket.send(b"Authentication failed.\n")
        f = open("/var/log.orionrexec.log","a")
        f.write(os.popen('date').read().strip() + " ~ Unsuccessful login from IP: {client_address}\n")
        f.close()
        return False

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

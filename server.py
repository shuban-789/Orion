import socket
import spwd
import os
import subprocess
import crypt
import threading
import time

def read_shell_output(shell_process, client_socket, stop_flag):
    for line in shell_process.stdout:
        if stop_flag.is_set():
            break
        client_socket.send(line)

def shell(client_socket):
    client_socket.send(b"Shell access granted. Type 'exit' to exit the shell.\n")
    shell_process = subprocess.Popen(['/bin/bash'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stop_flag = threading.Event()
    output_thread = threading.Thread(target=read_shell_output, args=(shell_process, client_socket, stop_flag))
    output_thread.start()

    while True:
        time.sleep(0.2)
        client_socket.send(b">>> ")
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

    try:
        PASSWORD = spwd.getspnam(username)
    except KeyError:
        client_socket.send(b"User not found.\n")
        return False

    client_socket.send(b"Enter the password: ")
    password_attempt = client_socket.recv(1024).strip().decode("utf-8")

    if crypt.crypt(password_attempt, PASSWORD.sp_pwdp) == PASSWORD.sp_pwdp:
        f = open("/var/log/orionrexec.log", "a")
        f.write(os.popen('date').read().strip() + f" ~ Successful login by user: {username} IP: {client_address}\n")
        f.close()
        return True
    else:
        f = open("/var/log/orionrexec.log", "a")
        f.write(os.popen('date').read().strip() + f" ~ Unsuccessful login from IP: {client_address}\n")
        f.close()
        client_socket.send(b"Authentication failed.\n")
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

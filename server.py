import socket
import os
import crypt
import spwd
import getpass
import sys
import subprocess

def hash_password(passw):
    return crypt.crypt(passw) # Hash string to unix hash

def shell(client_socket):
    client_socket.send(b"Shell access granted. Type 'exit' to exit the shell.\n") # Send message to client that access is granted, as function is called upon successful authentication
    shell_process = subprocess.Popen(['/bin/bash'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Inititate bash shell, make sure input, output, and errors of commands can be communicated
    while True:
        command = client_socket.recv(1024).decode("utf-8") # Recieve command from client
        if command.lower() == "exit": # If client wants to exit, break the command loop
            break
        shell_process.stdin.write(command.encode("utf-8") + b'\n') # Write command to shell
        shell_process.stdin.flush() 
        output = shell_process.stdout.readline().decode("utf-8") # Read output
        client_socket.send(output.encode("utf-8")) # Relay output to client
    shell_process.stdin.close() # Close input, output, and error
    shell_process.stdout.close()
    shell_process.stderr.close()
    shell_process.kill() # Kill process and close sshell
    client_socket.send(b"Shell session closed.\n")
    
def authenticate(client_socket, client_address):
    client_socket.send(b"Enter the username: ") # Prompt for user
    username = client_socket.recv(1024).strip().decode("utf-8") # Recieve username
    
    try:
        PASSWORD = spwd.getspnam(username).sp_pwdp # Get hash of password for that username
    except KeyError:
        client_socket.send(b"User not found.\n") # But if user does not exist, relay that information
        return False

    client_socket.send(b"Enter the password: ") # Prompt for password
    password_attempt = client_socket.recv(1024).strip().decode("utf-8") # Get password

    if hash_password(password_attempt) == PASSWORD: # Check if hashes match
        f = open("/var/log/orionrexec.log","a") # Append information about successful login into the log file
        f.write(os.popen('date').read().strip() + " ~ Successful login by user: " + username + " IP: {client_address}\n")
        f.close()
        return True
    else:
        client_socket.send(b"Authentication failed.\n") # Append information about unsuccessful login into the log file
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

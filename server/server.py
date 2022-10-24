import socket
import random
import string
from threading import Thread
import os
import shutil
from pathlib import Path


FORMAT = 'utf-8'

def get_working_directory_info(working_directory):
    dirs = '\n-- ' + '\n-- '.join([i.name for i in Path(working_directory).iterdir() if i.is_dir()])
    files = '\n-- ' + '\n-- '.join([i.name for i in Path(working_directory).iterdir() if i.is_file()])
    dir_info = f'Current Directory: {working_directory}:\n|{dirs}{files}'
    return dir_info


def generate_random_eof_token():
    random_eof_token = f"<{''.join(random.choices(string.ascii_lowercase, k=8))}>"
    print("random token is "+random_eof_token)
    return(random_eof_token)


def receive_message_ending_with_token(active_socket, buffer_size, eof_token):
    data = bytearray()
    while True:                             # keep receiving until we get '<EOF>'
        packet = active_socket.recv(buffer_size)
        data.extend(packet)
        if packet.decode()[-10:] == eof_token :
            data = data[:-10]
            break
    
    return data

def handle_cd(current_working_directory, new_working_directory):
    print("old is "+current_working_directory)
    if new_working_directory != '..':
        os.chdir(f"{current_working_directory}/{new_working_directory}")
        print("we are here")

    else:
        dn = os.path.dirname(os.getcwd())
        os.chdir(dn)
        print("we are not here")


    print("new is ",os.getcwd())   
    return(os.getcwd())


def handle_mkdir(current_working_directory, directory_name):
    print("old is "+current_working_directory)

    path = os.path.join(current_working_directory,directory_name)
    os.mkdir(path)
    print("new is "+os.getcwd())
    return(os.getcwd())
    # raise NotImplementedError('Your implementation here.')


def handle_rm(current_working_directory, object_name):
    print("old is "+current_working_directory)

    path = os.path.join(current_working_directory,object_name)
    shutil.rmtree(path)

    print("new is "+os.getcwd())
    return(os.getcwd())

    # raise NotImplementedError('Your implementation here.')


def handle_ul(current_working_directory, file_name, service_socket, eof_token):
    file_name = os.path.basename(file_name)

    with open(file_name, "wb") as f:
        file_content = receive_message_ending_with_token(service_socket,1024,eof_token)
        print("we are getting the content ",file_content)
        # write to the file the bytes we just received
        f.write(file_content)
    return

def handle_dl(current_working_directory, file_name, service_socket, eof_token):
    with open(file_name.decode(), 'rb') as f:
            file_content = f.read()
    file_content_with_token = file_content + eof_token.encode(FORMAT)
    service_socket.sendall(file_content_with_token)
    return current_working_directory

class ClientThread(Thread):
    def __init__(self, service_socket : socket.socket, address : str):
        Thread.__init__(self)
        self.service_socket = service_socket
        self.address = address

    def run(self):
        print ("Connection from : ", self.address)


        eof_token = generate_random_eof_token()
        self.service_socket.send(eof_token.encode(FORMAT))

        working_directory = os.getcwd()
        print(get_working_directory_info(working_directory))
        # working_directory = get_working_directory_info(working_directory)
        self.service_socket.send(working_directory.encode(FORMAT))


        while True:
            command_received = receive_message_ending_with_token(self.service_socket,1024,eof_token).decode(FORMAT)

            if not command_received:
                break

            if 'cd' in command_received:
                changed_directory = handle_cd(working_directory,command_received.split()[1])
                self.service_socket.send(changed_directory.encode(FORMAT))
            elif 'mkdir' in command_received:
                changed_directory =handle_mkdir(working_directory,command_received.split()[1])
                self.service_socket.send(changed_directory.encode(FORMAT))
            elif 'rm' in command_received:
                changed_directory = handle_rm(working_directory,command_received.split()[1])
                self.service_socket.send(changed_directory.encode(FORMAT))
            elif 'ul' in command_received:
                changed_directory = handle_ul(working_directory,command_received.split()[1],self.service_socket,eof_token)
                self.service_socket.send(changed_directory.encode(FORMAT))
            elif 'dl' in command_received:
                changed_directory = handle_dl(working_directory,command_received.split()[1],self.service_socket,eof_token)
                self.service_socket.send(changed_directory.encode(FORMAT))

            else:
                print('nothing happened')


def main():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 65431

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()

            client_thread = ClientThread(conn, addr)
            client_thread.start()



if __name__ == '__main__':
    main()



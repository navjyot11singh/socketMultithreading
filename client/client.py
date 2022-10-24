from pydoc import cli
import socket


FORMAT='utf-8'

def receive_message_ending_with_token(active_socket, buffer_size, eof_token):

    data = bytearray()
    while True:                             # keep receiving until we get '<EOF>'
        packet = active_socket.recv(buffer_size)
        data.extend(packet)
        if packet.decode()[-10:] == eof_token :
            data = data[:-10]
            break
    
    return data


def initialize(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print('Connected to server at IP:', host, 'and Port:', port)
    eof_token_received = client.recv(1024).decode(FORMAT)
    print('Handshake Done. EOF is:', eof_token_received)
    return eof_token_received ,client


def issue_cd(command_and_arg, client_socket, eof_token):
    client_socket.send((command_and_arg+eof_token).encode(FORMAT))

    response_received = client_socket.recv(1024)

    print("CWD: ",response_received.decode(FORMAT))
    pass
    # raise NotImplementedError('Your implementation here.')


def issue_mkdir(command_and_arg, client_socket, eof_token):
    print("hi we got in issue_mkdir ",command_and_arg,client_socket)
    client_socket.send((command_and_arg+eof_token).encode(FORMAT))

    response_received = client_socket.recv(1024)
    print("CWD: ",response_received.decode(FORMAT))
    pass


def issue_rm(command_and_arg, client_socket, eof_token):
    print("hi we got in issue_rm ",command_and_arg,client_socket)
    client_socket.send((command_and_arg+eof_token).encode(FORMAT))

    response_received = client_socket.recv(1024)
    print("CWD: ",response_received.decode(FORMAT))
    pass


def issue_ul(command_and_arg, client_socket, eof_token):
    client_socket.send((command_and_arg+eof_token).encode(FORMAT))

    with open(command_and_arg.split()[1], 'rb') as f:
        file_content = f.read()
    file_content_with_token = file_content + eof_token.encode(FORMAT)
    client_socket.sendall(file_content_with_token)
    return
    """
    Sends the full ul command entered by the user to the server. Then, it reads the file to be uploaded as binary
    and sends it to the server. The server creates the file on its end and sends back the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    # raise NotImplementedError('Your implementation here.')


def issue_dl(command_and_arg, client_socket, eof_token):

    client_socket.send((command_and_arg+eof_token).encode(FORMAT))
    with open(command_and_arg.split()[1], "wb") as f:
        file_content = receive_message_ending_with_token(client_socket,1024,eof_token)
        print("we are getting the content ",file_content)
        # write to the file the bytes we just received
        f.write(file_content)
    
    return

    """
    Sends the full dl command entered by the user to the server. Then, it receives the content of the file via the
    socket and re-creates the file in the local directory of the client. Finally, it receives the latest cwd info from
    the server.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    :return:
    """
    # raise NotImplementedError('Your implementation here.')


def main():
    #STEP-1
    HOST = socket.gethostbyname(socket.gethostname()) 
    PORT = 65431

    eof_token_received ,s = initialize(HOST,PORT)

    while True:
        user_input = input('Enter your input ')
        if 'cd' in user_input:
            issue_cd(user_input,s,eof_token_received)
        elif 'mkdir' in user_input:
            issue_mkdir(user_input,s,eof_token_received)
        elif 'rm' in user_input:
            issue_rm(user_input,s,eof_token_received)
        elif 'dl' in user_input:
            issue_dl(user_input,s,eof_token_received)
        elif 'ul' in user_input:
            issue_ul(user_input,s,eof_token_received)
        elif 'exit' in user_input:
            break
        else:
            print('Not a valid command')



        # get user input

        # call the corresponding command function or exit


    print('Exiting the application.')


if __name__ == '__main__':
    main()
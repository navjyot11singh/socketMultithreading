# socketMultithreading

In this program we are implementing sockets using python. The project supports multithreading is
performing basic terminal tasks like cd, mkdir, upload, download and remove. This is one of the 
best examples to learn about multithreading in sockets.

# **Server**: ******The****** server initializes its socket and internal variables and awaits upcoming connections
from clients. When a client connects to the designated socket (pre-defined), the server handles
the connection in a new thread and awaits connections from other clients. In the client thread,
the server and client interact with each other to execute the upcoming client commands until the
client terminates. When initializing the connection, the server sends the client a random token of
size 10 bytes, which both the client and server will use to indicate the end of their messages
(EOF). The server sends the CWD info to the client before receiving each command. To support
multiple clients, the server maintains a cwd variable per client.


**Client** : The client initializes its internal variables, establishes a connection to the designated
server socket, gets the random EOF token, and awaits the user's command. Before each
command, the client displays the received CWD info from the server to the user. After the server
has executed the command and sent back the latest directory info, the client displays it to the
user and awaits the next command. If the user enters the exit command, the client terminates
the connection exits gracefully. For simplicity of our application, we assume a fixed current
working directory on the client, i.e. the user might upload/download files to/from the CWD on
the server (mutable), but these files are uploaded/downloaded from/to the directory where the
client script is executed (immutable).

import socket

host_name = socket.gethostname()
print(host_name)
print(socket.gethostbyname(host_name))

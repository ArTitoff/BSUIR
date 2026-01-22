# from socket import *
# serverName = 'hostname'
# serverPort = 12000
# clientSocket = socket(AF_INET, SOCK_DGRAM)
# message = input('Input lowercase sentence:')
# clientSocket.sendto(message.encode(),(serverName,
# serverPort))
# modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
# print(modifiedMessage)
# clientSocket.close()

from socket import *

serverName = 'localhost'  # или '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Input lowercase sentence:')
# Кодируем строку в байты перед отправкой
clientSocket.sendto(message.encode(), (serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
# Декодируем байты обратно в строку для вывода
print(modifiedMessage.decode())

clientSocket.close()
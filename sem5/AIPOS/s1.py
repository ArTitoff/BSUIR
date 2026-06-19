# from socket import *
# serverPort = 12000
# serverSocket = socket(AF_INET, SOCK_DGRAM)
# serverSocket.bind(('', serverPort))
# print("The server is ready to receive")
# while 1:
#     message, clientAddress = serverSocket.recvfrom(2048)
#     decoded_message = message.decode()
#     # Преобразуем в верхний регистр
#     modifiedMessage = decoded_message.upper()
#     serverSocket.sendto(modifiedMessage.encode(), clientAddress)

from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    # Декодируем полученное сообщение
    decoded_message = message.decode()
    # Преобразуем в верхний регистр
    modifiedMessage = decoded_message.upper()
    # Кодируем обратно в байты для отправки
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
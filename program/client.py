import socket
import threading
from time import sleep
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#создаём сокет
sock.bind(('', 0))
server = '127.0.0.1', 4321 #сервер для подключения
def choise_name(): # как общаться без имени?
    while True:
        xname = input(str('Введите ваш никнейм) \n'))
        if xname == None:
            print('Имя есть у каждого, вводи, сцука \n <. \t- _ - \t.>')
        else:
            return xname
sock.sendto(f'{choise_name()}'.encode('utf-8'), server) # отправляем имя на сервак

def inputt(): #просто функция ввода
    return input('Вы: ')

while True: # проверка на уникальность никнейма
        data = sock.recv(1024)
        data = str(data.decode('utf-8'))
        if data == '-1':
            print('\nНикнейм занят, пожалуйста, введите другой! \n')
            sock.sendto(f'{choise_name()}'.encode('utf-8'), server)
        else:
            print('\n' + data)
            break

print('Если хотите увидеть список комманд, введите -comms')
sleep(1)

global thread_stop #попытка научиться стопорить поток

def read_msg(): #функция для чтения входящих сообщений
    while 1:
        data = sock.recv(1024)
        data = str(data.decode('utf-8'))
        print('\n' + data)

thread = threading.Thread(target=read_msg)#через потоки запускаем функцию
thread.start()

while True: #функция считывания ввода и аргументов для клиента 
    sleep(0.5)
    messege = inputt()
    if messege == '-q':
        sock.sendto('-q'.encode('utf-8'), server)
        break
    elif messege == '-comms':
        print('\nСписок комманд и флагов: \n/users? - Пользователи онлайн \n$ - Сообщение всем \n-to xname - личное сообщение пользователю \n')
    else:
        sock.sendto(f'{messege}'.encode('utf-8'), server)

sock.close()# закрывем сокет
thread_stop = True #попытка закрыть поток
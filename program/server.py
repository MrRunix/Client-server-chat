import socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #ставим сокет
sock.bind (('127.0.0.1',4321)) #прописываем адрес сервера
xnames_adds = {} #создаём словарь для хранения адресов и ников
print ('Start Server')

while 1:
    data, addres = sock.recvfrom(1024) #принимаем сообщение с адресом отправления
    data = str(data.decode('utf-8')) #дешифруем само сообщение
    print(data, addres)
    if (('$' in data) and ('/users?' in data)) or ('/users?' in data) and ('-to ' in data) or ('$' in data) and ('-to ' in data): #проверка пользователя на адекватность
        sock.sendto('Пожалуйста, проверьте правильность написания флагов и их наличие'.encode('utf-8'), addres)
    if addres not in xnames_adds.keys(): #проверяем, есть ли такой такой пользователь
        print("prof")
        if (data in xnames_adds.values()) and (addres not in xnames_adds.keys()): # проверка на уникальность никнейма
            sock.sendto("-1".encode('utf-8'), addres) 
        else:
            if len(xnames_adds) == 0:                                           #
                sock.sendto("Welcome, u're first))".encode('utf-8'), addres)    #
            else:                                                               # говорим пользователю, об успешном доступе на сервер
                sock.sendto("Welcome!".encode('utf-8'), addres)                 #
            xnames_adds.update({addres:data}) # Добавляем пользователя в словарь
            print(f'{data} Connect to server!')
    elif data == '-q':                                      #
        print(f'{xnames_adds.get(addres)}, disconnect!')    # если пользователь желает выйти, удаляем его из словаря
        del xnames_adds[addres]                             #
    elif '$' in data[0]:        # проверка флага на ширик
        data = data[2::]
        for client in xnames_adds.keys(): # в цикле отправляем всем клиентам
            if client == addres:
                continue
            else:
                sock.sendto((f'From {xnames_adds.get(addres)}: {data} (all)').encode('utf-8'), client)
    elif '/users?' in data: #проверка на команду выдачи пользователей в сети
        usrs = ''
        for i in xnames_adds.values(): # избавляемся от лишнего синтаксиса
            usrs = usrs + f'{i} \n' 
        sock.sendto((f'Users: \n{usrs}').encode('utf-8'), addres)
    elif '-to ' in data: # проверка на флаг личной отправки
        s = list(data.split(' '))
        print(s)
        if s[1] not in xnames_adds.values(): # проверка на существование пользователя
            sock.sendto(('Пользователь не найден(').encode('utf-8'), addres)
        print(s[1], addres)
        if xnames_adds.get(addres) == s[1]: # проверка на отправление самому себе
            print('oaoao', addres)
            sock.sendto('Тебе настолько одиноко? \nСходи прогуляйся, че ты здесь торчишь?'.encode('utf-8'), addres)
        else:
            for clin in xnames_adds.keys(): # поиск адреса отправки
                if xnames_adds.get(clin) == s[1]:
                    s = s[2::]
                    data = ''.join(map(str, s))#пересобираем сообщение в комфортный вид
                    sock.sendto((f'From {xnames_adds.get(addres)}: {data} (personal)').encode('utf-8'), clin)
                    break
    elif ('down server' in data) and (xnames_adds.get(addres) == 'serveradmin'): #проверка на адекватность администратора сервера
        print('9')
        print('Server down, thks admin)')
        break
    else:
        print(10)
        sock.sendto('Пожалуйста, проверьте правильность написания флагов и их наличие)'.encode('utf-8'), addres)

for i in xnames_adds.keys(): #отправка сообщений об отключении сервера
    sock.sendto('Всем спасибо, сервер лёг)'.encode('utf-8'), i)
sock.close()
#down server - положить сервак(доступно не всем)
import psycopg2

connection = psycopg2.connect(
    database='phone store',
    user='postgres',
    password='j78fxkl21',
    host='localhost',
    port='5432'
)

print(connection)
cursor = connection.cursor()

Q_createUsers = """
CREATE TABLE IF NOT EXISTS Users (
    id serial NOT NULL,
    surname varchar(50) NOT NULL,
    name varchar(50) NOT NULL,
    patronymic varchar(50) NOT NULL,
    login varchar(50) NOT NULL,
    password char(30) NOT NULL,
    function varchar(50) NOT NULL
);
"""
# cursor.execute(Q_createUsers)
# connection.commit()

Q_insertUsers = """
INSERT INTO users (surname, name, patronymic, login, password, function) VALUES
('Смирнов', 'Игорь', 'Петрович', 'Dg23dW%y', 'JH56gt%df', 'admin');
"""
# cursor.execute(Q_insertUsers)
# connection.commit()

Q_createPhone = """
CREATE TABLE IF NOT EXISTS Phone (
    id serial NOT NULL,
    model varchar(50) NOT NULL,
    processor varchar(50) NOT NULL,
    RAM varchar(50) NOT NULL,
    built_memory varchar(50) NOT NULL
);
"""

Q_insertPhone = """
INSERT INTO phone (model, processor, RAM, built_memory) VALUES
('Honor X7', 'Snapdragon 680', '6 Г', '128 ГБ'),
('Samsung Galaxy A32', 'MediaTek Helio G80', '6 Гб', '128 ГБ'),
('Xiaomi 12T', 'Dimensity 8100 Ultra', '8 Гб', '128 ГБ'),
('Motorola Edge 30 Pro', 'Snapdragon 8 Gen 1', '12 Гб', '256 ГБ');
"""
# cursor.execute(Q_createPhone)
# cursor.execute(Q_insertPhone)
# connection.commit()

Q_createShopping_phone = """
CREATE TABLE IF NOT EXISTS Shopping_phone (
    id serial NOT NULL,
    model varchar(50) NOT NULL,
    processor varchar(50) NOT NULL,
    RAM varchar(50) NOT NULL,
    built_memory varchar(50) NOT NULL
);
"""
# cursor.execute(Q_createShopping_phone)
# connection.commit()

print('*' * 50, '~' * 18, '*' * 50)
print('*' * 50, 'МАГАЗИН СМАРТФОНОВ', '*' * 50)
print('*' * 50, '~' * 18, '*' * 50)


def enter():
    while True:
        try:
            print('Авторизуйтесь или зарегистрируйтесь в системе\nДля выхода из программы введите "0"')
            aut_end = input(' Для авторизации введите "1"\nДля регистрации введите "2"\n: ')
            if aut_end == '0':
                break
            elif aut_end == '1' and aut_end != '':
                log = input('Введите логин\n: ')
                passw = input('Введите пароль\n: ')
                cursor.execute(
                    "SELECT exists(SELECT * FROM users WHERE login=%s)",
                    (log, )
                )
                log_int = cursor.fetchone()[0]
                # print(log_int)
                if log_int == True and log != '':
                    cursor.execute(
                        "SELECT EXISTS(SELECT * FROM users WHERE password = %s)",
                        (passw,)
                    )
                    passw_int = cursor.fetchone()[0]
                    # print(passw_int)
                    if passw_int == True and passw != '':
                        print(f'Поздравляю {log}! \nВы вошли в систему!')
                        cursor.execute(
                            "SELECT exists(SELECT * FROM users WHERE function = 'admin' AND login = %s)",
                            (log,)
                        )
                        funct_admin = cursor.fetchone()[0]
                        # print('admin = ', funct_admin)
                        if funct_admin == True:
                            admin_function()
                            break
                        cursor.execute(
                            "SELECT exists(SELECT * FROM users WHERE function = 'edit_user' AND login = %s)",
                            (log,)
                        )
                        funct_edit_user = cursor.fetchone()[0]
                        # print('edit_user = ', funct_edit_user)
                        if funct_edit_user == True:
                            delete_shopping_phone()
                        else:
                            purchase_phone()
                            break
                    else:
                        print('Логин или пароль введены неверно!')
                        continue
                else:
                    print('Логин или пароль введены неверно!')
                    continue
            elif aut_end == '2' and aut_end != '':
                print('Для регистрации введите свои данные ')
                surn = input('Фамилия\n: ')
                name = input('Имя\n: ')
                patr = input('Отчество\n: ')
                log_reg = input('Логин\n: ')
                while True:
                    passw_reg1 = input('Введите пароль\n: ')
                    passw_reg2 = input('Введите пароль повторно\n: ')
                    if passw_reg1 != passw_reg2:
                        print('\nВведенные пароли не совпадают!\nПопробуйте еще раз')
                        continue
                    else:
                        print(f'\nПоздравляю {log_reg}!\nВы успешно зарегистрировались! \nДля входа введите логин и пароль')
                        while True:
                            log = input('Введите логин\n: ')
                            passw = input('Введите пароль\n: ')
                            if log in log_reg and passw in passw_reg2:
                                us = 'user'
                                cursor.execute(
                                    '''INSERT INTO users (surname, name, patronymic, login, password, function) 
                                    VALUES (%s, %s, %s, %s, %s, %s)''',
                                    (surn, name, patr, log, passw, us)
                                )
                                connection.commit()
                                purchase_phone()
                                break
                            else:
                                print('Вы ввели неверно логин или пароль')
                                continue
                        break
                break
            elif aut_end == '0':
                print('Вы вышли из системы! \nДосвидания!')
                break
            else:
                print('Вы ввели неверное значение')
                continue
        except ValueError:
            continue



def users():
    print('\n        Зарегистрированные пользователи')
    cursor.execute(
        "SELECT * FROM users"
    )
    items_user = cursor.fetchall()
    for row in items_user:
        print(row)


def admin_function():
    print('Привет! admin!')
    while True:
        try:
            print('Выберите действие')
            change = int(input('Для выхода в главное меню введите "0"\nДля добавления товара введите "1"\n'
                                'Для удаления товара введите "2"\nДля просмотра пользователей введите "3"\n'
                                'Для изменения функций пользователя введите "4"\n: '))
            if change == 0:
                enter()
                break
            elif change == 1:
                print(phone())
                print('Для выхода в предыдущее меню введите "0"\n\nВведите данные смартфона')
                model = input('\tМодель\n: ')
                if model == "0" or model == '':
                    continue
                else:
                    processor = input('\n\tПроцессор\n: ')
                    if processor == "0" or processor == '':
                        continue
                    else:
                        RAM = input('\n\tОперативная память\n: ')
                        if RAM == "0" or RAM == '':
                            continue
                        else:
                            built_memory = input('\n\tВстроенная память\n: ')
                            if built_memory == "0" or built_memory == '':
                                continue
                            else:
                                cursor.execute(
                                    '''INSERT INTO phone (model, processor, RAM, built_memory) 
                                    VALUES (%s,%s,%s,%s)''',
                                    (model, processor, RAM, built_memory)
                                )
                                connection.commit()
                                print(f'Товар {model} добавлен в базу данных!')
                                continue
            elif change == 2:
                print(phone())
                print('Для выхода в предыдущее меню введите "0"')
                try:
                    id_phone = int(input('Введите номер id товара для удаления\n: '))
                    if id_phone == 0:
                        continue
                    else:
                        cursor.execute(
                            "DELETE FROM phone WHERE id = %s",
                            (id_phone,)
                        )
                        connection.commit()
                        print(f'Товар {id_phone} удален из базы данных!')
                        continue
                except ValueError:
                    continue
            elif change == 3:
                print('%' * 28, 'Выведены все зарегистрированные пользователи', '%' * 28)
                print(users())
                print('%' * 100)
                print('%' * 100)
                continue
            elif change == 4:
                print(users())
                print('Выберете номер Id пользователя, у которого хотите поменять функцию\n'
                      'Для выхода в предыдущее меню введите "0"')
                try:
                    id_user = int(input('Введите номер id пользователя\n: '))
                    if id_user == 0:
                        continue
                    elif id_user == 1:
                        print('admin нельзя менять функцию!')
                        continue
                except ValueError:
                    continue
                try:
                    change_user = int(input('Для предоставления пользователю права "edit_user" введите "1"\n'
                                            'Для предоставления права user" введите "2"\n: '))
                    if change_user == 1:
                        cursor.execute(
                            "UPDATE users SET function = 'edit_user' WHERE id = %s",
                            (id_user,)
                        )
                        connection.commit()
                        print(f'User {id_user} предоставлено право Edit_user!')
                        continue
                    elif change_user == 2:
                        cursor.execute(
                            "UPDATE users SET function = 'user' WHERE id = %s",
                            (id_user,)
                        )
                        connection.commit()
                        print(f'Edit_user {id_user} предоставлено право User!')
                        continue
                    else:
                        print('Вы ввели неверное значение')
                        continue
                except ValueError:
                    continue
            else:
                print('Вы ввели неверное значение')
                continue
        except ValueError:
            continue


def phone():
    print(' %' * 80, '\n\t\t\t\t\t\t\tСмартфоны в наличии\n', '%' * 80)
    cursor.execute(
        "SELECT * FROM phone"
    )
    items = cursor.fetchall()
    for row in items:
        print(row)


def purchase_phone():
    while True:
        print(phone())
        print(shop_phone())
        print('Для выхода в главное меню введите "0"')
        try:
            ch_ph = int(input('\nВведите номер Id выбранного смартфона для покупки\n: '))
            if ch_ph != 0:
                cursor.execute(
                    '''INSERT INTO shopping_phone (model, processor, RAM, built_memory)
                                SELECT model, processor, RAM, built_memory FROM phone WHERE id = %s''',
                    (ch_ph,)
                )
                connection.commit()
                continue
            elif ch_ph == 0:
                enter()
                break
        except ValueError:
            continue


def delete_shopping_phone():
    while True:
        print(shop_phone())
        print('Для выхода в главное меню введите "0"')
        try:
            id_phone = int(input('Введите номер id товара для удаления\n: '))
            if id_phone != 0:
                cursor.execute(
                    "DELETE FROM shopping_phone WHERE id = %s",
                    (id_phone,)
                )
                connection.commit()
                print(f'Товар {id_phone} удален из базы данных!')
                continue
            elif id_phone == 0:
                break
        except ValueError:
            continue


def shop_phone():
    print(' %' * 80, '\n\t\t\t\t\t\t\tКорзина покупок\n', '%' * 80)
    cursor.execute(
        "SELECT * FROM shopping_phone"
    )
    sh_phone = cursor.fetchall()
    for row in sh_phone:
        print(row)


enter()
cursor.close()
connection.close()

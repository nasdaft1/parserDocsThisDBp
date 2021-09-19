__author__ = 'JaxsT'

import firebirdsql
import os
import socket


class SearchDb:
    connect_db = None

    def __init__(self, path_db):
        user_db = 'sysdba'              # логин  БД FIREBERD
        password_db = 'masterkey'       # пароль БД FIREBERD
        charset_db = 'WIN1251'          # пароль БД FIREBERD
        if SearchDb.checking_possible_connection(path_db):
            try:
                parameters_connect_db = firebirdsql.connect(
                    dsn=path_db,
                    user=user_db,
                    password=password_db,
                    charset=charset_db
                )
                self.connect_db = parameters_connect_db.cursor()
            except ConnectionError:
                print('\033[1;31Нет соединения с базой данных [' + path_db + ']\033[0m')

    @staticmethod
    def test_connect_localhost_path(path_file):
        # Проверка файла на компьютере LOCALHOST
        if os.path.exists(path_file):
            return True     # фаил найден
        print('\033[1;31mERROR: ->необнаружен файла на компьютере ' + path_file + '  \033[0m')
        return False

    @staticmethod
    def test_connect_ip(ip_connect):
        # функция проверки доступа к файлу на компьютере и компьютера в сети
        sock = socket.socket()
        try:
            sock.settimeout(0.01)     # установка времени ожидания
            sock.connect((ip_connect, 23))
            sock.close()
            return True
        except socket.timeout:
            print('\033[1;31mERROR: нет подключения к БД IP адресу ' + ip_connect + '  \033[0m')
            sock.close()
            return False

    @staticmethod
    def checking_possible_connection(path_db_connect):
        # разбивка строки на ip и пути
        ip = path_db_connect[:path_db_connect.find(':')].upper()
        disk_path = path_db_connect[path_db_connect.find('/')+1:]
        if ip == 'LOCALHOST':
            if not SearchDb.test_connect_localhost_path(disk_path):
                return False
        else:
            if not SearchDb.test_connect_ip(ip):
                return False
        return True

    # получить return с одной строкой даннами
    def requesting_data_one(self, command_sql):     # функция для получения однострочного кортежа данных
        try:
            self.connect_db.execute(command_sql)        # SQL запрос в БД
        except firebirdsql.Error:
            return None
        return self.connect_db.fetchone()

    def requesting_data_list(self, command_sql):    # функция для получения много строчного кортежа данных
        # получить return с многострочными даннами
        try:
            self.connect_db.execute(command_sql)        # SQL запрос в БД
        except firebirdsql.Error:
            return None
        return self.connect_db.fetchall()

    @staticmethod
        # метод для получение данных определенного (index) поля таблици базы данных
    def redo_and_check(data, index):
        try:
            if data[index] is not None:
                result = str(data[index]).rstrip()  # если поле не None переводим в str и убираем пробелы
            else:
                result = ''
        except IndexError:  # при ошибке к достепу к полю оставляем пустое поле
            result = ''
        return result

    @staticmethod
    # формирование данных из кортэжа data/ некоторые базы данных не содержат поля district - (поселок, район)
    def address_format(data, street, house_num, bilding, korpus, flat_num, district=None):
        street_str = SearchDb.redo_and_check(data, street)       # улица
        bilding_str = SearchDb.redo_and_check(data, bilding)     # строение
        korpus_str = SearchDb.redo_and_check(data, korpus)       # корпус здания
        flat_num_str = SearchDb.redo_and_check(data, flat_num)   # номер здания
        if flat_num_str != '':
            flat_num_str = '-' + flat_num_str
        if bilding_str != '':
            bilding_str = ' стр.' + bilding_str
        if korpus_str != '':
            korpus_str = '\\' + korpus_str
        if district is not None:
            district_str = SearchDb.redo_and_check(data, district)
            if (district_str != '') and (street_str != ''):
                district_str += ', '
        else:
            district_str = ''
        s = district_str + street_str + ' ' + SearchDb.redo_and_check(data, house_num) + bilding_str + korpus_str + flat_num_str
        return s



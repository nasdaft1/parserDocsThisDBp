__author__ = 'JaxsT'
import fdb

class connect_and_work_db():
    #__connect_db= None
    def __init__(self,path_db):
        user_db=r'sysdba'                                # логин БД FIREBERD
        password_db=r'masterkey'                         # пароль БД FIREBERD
        parameters_connect_db = fdb.connect(
                            dsn=path_db,
                            user=user_db,
                            password=password_db)
        self.connect_db = parameters_connect_db.cursor()

    def requesting_data_one(self,command_SQL): # функция для получения однострочного кортежа данных
        self.connect_db.execute(command_SQL) # SQL запрос в БД
        return self.connect_db.fetchone()

    def requesting_data_list(self,command_SQL): # функция для получения много строчного кортежа данных
        self.connect_db.execute(command_SQL) # SQL запрос в БД
        return self.connect_db.fetchall()


    # формирование данных из кортэжа data/ некоторые базы данных не содержат поля district - (поселок, район)
    def address_format(self, data, street ,house_num, bilding, korpus, flat_num, district = None):
        street_str   = redo_and_check(data, street)  # улица
        bilding_str  = redo_and_check(data, bilding) # строение
        korpus_str   = redo_and_check(data, korpus)  # корпус здания
        flat_num_str = redo_and_check(data, flat_num)# номер здания

        if (flat_num_str != '') : flat_num_str = '-' + flat_num_str
        if (bilding_str  != '') : bilding_str  = ' стр.' + bilding_str
        if (korpus_str   != '') : korpus_str   = '\\' + korpus_str
        if district is not None:
            district_str = redo_and_check(data, district)
            if (district_str != '') and (street_str != '') : district_str +=', '
        else: district_str=''
        s = district_str + street_str + ' ' + redo_and_check(data, house_num) + bilding_str + korpus_str + flat_num_str
        return s

def redo_and_check(data,index):
    try:
        if data[index] is not None : result = str(data[index]).rstrip() # если поле не None переводим в str и убираем пробелы
        else: result =''
    except: # при ошибке к достепу к полю оставляем пустое поле
        result =''
    return result

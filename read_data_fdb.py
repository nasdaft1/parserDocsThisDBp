__author__ = 'JaxsT'

from SearchDB import connect_and_work_db
from SearchDB import redo_and_check

class work_db_fdb:

    def read_data_fdb(self, path_db, card):
        self.data_dictionary = {} # словарь для работы с процедурой
        db = connect_and_work_db(path_db)
        command_SQL = 'select ANOTHERCUST.custname, ANOTHERCUST.id_cust, objects.label, dogovora.dognum, '\
                      +' ANOTHERCUST.objid from ANOTHERCUST, objects, dogovora where objects.id = ANOTHERCUST.custclassid '\
                      +' and dogovora.id_dog = ANOTHERCUST.id_dog and (ANOTHERCUST.custmode=1) and ANOTHERCUST.CUSTNUM=' + card
        data= db.requesting_data_one(command_SQL)
        data_id_name_object = redo_and_check(data,0) #в словарь добавляется название объекта
        data_id_cust =        redo_and_check(data,1)  #id_cust
        #self.data_dictionary['ed']          = pult.upper()
        self.data_dictionary['card']        = card   #в словарь добавляется позывной объекта
        self.data_dictionary['type_object'] = redo_and_check(data,2).upper()  #в словарь добавляется тип объекта
        # от типа объекта заполняются определенные поля
        if (self.data_dictionary['type_object'] == 'КВАРТИРА') or (self.data_dictionary['type_object'] == 'МХЛИГ'):
            #в словарь добавляется названание объекта для физического лица
            self.data_dictionary['type_object_physical'] = data_id_name_object
        else:
            #в словарь добавляется названание объекта для юридического лица
            self.data_dictionary['type_object_legal'] = data_id_name_object
        self.data_dictionary['cont']    = redo_and_check(data,3)  #в словарь добавляется договор объекта
        data_id_object =      redo_and_check(data,4)  #id_obj
        data= db.requesting_data_one('select podezd, floor, custdescription from anothercust_ext where id_cust=' + data_id_cust)
        self.data_dictionary['entrance'] = redo_and_check(data,0) #в словарь добавляется подъезд
        self.data_dictionary['floor']    = redo_and_check(data,1) #в словарь добавляется этаж
        self.data_dictionary['memo1']    = redo_and_check(data,2) #в словарь добавляется характеристики объекта
        data= db.requesting_data_one('select ops_type.title from ops,  ops_type where ops.type_ = ops_type.subtype_ and ops.id = ' + data_id_object)
        self.data_dictionary['type_ou']  = redo_and_check(data,0) #в словарь добавляется тип оконечного устройства
        command_SQL = 'SELECT (select labels.label from  labels where addresses.id_street = labels.id  ), '\
                      ' addresses.house_num, addresses.building, addresses.korpus, addresses.flat_num, '\
                      ' (select labels.label from  labels where addresses.id_settl = labels.id  ) '\
                      ' FROM addresses where  addresses.id_owner=' + data_id_cust
        data= db.requesting_data_one(command_SQL)
        #в словарь добавляется адрес объекта
        self.data_dictionary['address_object'] = db.address_format(data, 0, 1 ,2 ,3 ,4 ,5 ) #
        data= db.requesting_data_one('select phone from phones where phone_type=1 and id_owner=' + data_id_cust )
        self.data_dictionary['phone'] = redo_and_check(data,0) #в словарь добавляется телефон объекта
        # добавляем внутреннии select запросы для уменьшения кода и исключения ошибок при неполном заполнение таблиц данными
        command_SQL =    'SELECT xo.surname, xo.name, xo.patronymic, '\
                         '(select labels.label FROM labels where addresses.id_street = labels.id)'\
                         ', addresses.house_num,  addresses.building, addresses.korpus, addresses.flat_num, '\
                         'xo.comment, (select labels.label from  labels where addresses.id_settl = labels.id  ),'\
                         ' xo.id_xo FROM xo, addresses, anothercust_xo where addresses.id_owner=xo.id_xo '\
                         ' and anothercust_xo.id_xo =  xo.id_xo and anothercust_xo.id_cust ='  + data_id_cust
        data_human = db.requesting_data_list(command_SQL)
        line = 0
        for data in data_human:
            line+=1
            # словарь добавляется фамилия имя отческтво человека
            self.data_dictionary['name'+str(line)]     = redo_and_check(data ,0) + ' ' + redo_and_check(data ,1) + ' ' + redo_and_check(data ,2)
            self.data_dictionary['position'+str(line)] = redo_and_check(data ,8) # словарь добавляется комментарий по человеку
            self.data_dictionary['address'+str(line)]  = db.address_format(data ,3 ,4 ,5 ,6 ,7 ,9) # словарь добавляется адрес человека
            index_phone = redo_and_check(data ,10)
            if index_phone != 0:
                data_phones_list = db.requesting_data_list('select phone_type, phone from phones where  id_owner=' + index_phone )
                phone_all = ''
                # в зависимости от типа data_phones[0] устанавливаем приставку с типом к телефону
                for data_phones in data_phones_list:
                    if data_phones[0] == 1: phone_all += '  ' + str(data_phones[1]) + '\n'
                    if data_phones[0] == 3: phone_all += 'р.' + str(data_phones[1]) + '\n'
                    if data_phones[0] == 4: phone_all += 'c.' + str(data_phones[1]) + '\n'
            self.data_dictionary['phone'+str(line)] = phone_all[:-1] # удаляем последний символ
        command_SQL = 'select objects.ncn, objects.label from objects where objects.isactive = 1 and  objects.parid =' + data_id_object
        data = db.requesting_data_list(command_SQL)
        line = 0
        for cell in data:
            line+=1
            self.data_dictionary['Shn'+str(line)] = str(cell[0]) # номер шлейфа
            self.data_dictionary['Shm'+str(line)] = str(cell[1]) # описание шлейфа


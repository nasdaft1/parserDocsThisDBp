__author__ = 'JaxsT'

from SearchDB import SearchDb


class WorkDbFdb:
    data_dictionary = {}  # словарь для работы с процедурой
    data_id_object = ''
    data_id_cust = ''
    data_id_name_object = ''
    index_phone = ''

    def select_start(self, db, card):
        command_sql = 'select ANOTHERCUST.custname, ANOTHERCUST.id_cust, objects.label, dogovora.dognum, '\
            + 'ANOTHERCUST.objid from ANOTHERCUST, objects, dogovora where objects.id = ANOTHERCUST.custclassid '\
            + 'and dogovora.id_dog = ANOTHERCUST.id_dog and (ANOTHERCUST.custmode=1) and ANOTHERCUST.CUSTNUM=' + card
        data = db.requesting_data_one(command_sql)
        if data is None:
            print('\033[1;31mERROR:Карточка [' + card + '] не найдена\033[0m')
            return False
        self.data_id_name_object = db.redo_and_check(data, 0)    # в словарь добавляется название объекта
        self.data_id_cust = db.redo_and_check(data, 1)    # id_cust
        self.data_dictionary['card'] = card      # в словарь добавляется позывной объекта
        self.data_dictionary['type_object'] = db.redo_and_check(data, 2).upper()  # в словарь добавляется тип объекта
        # от типа объекта заполняются определенные поля
        if (self.data_dictionary['type_object'] == 'КВАРТИРА') or (self.data_dictionary['type_object'] == 'МХЛИГ'):
            # в словарь добавляется названание объекта для физического лица
            self.data_dictionary['type_object_physical'] = self.data_id_name_object
        else:
            # в словарь добавляется названание объекта для юридического лица
            self.data_dictionary['type_object_legal'] = self.data_id_name_object
        self.data_dictionary['cont'] = db.redo_and_check(data, 3)  # в словарь добавляется договор объекта
        self.data_id_object = db.redo_and_check(data, 4)  # id_obj
        return True

    def select_address(self, db):
        data = db.requesting_data_one('select podezd, floor, custdescription from anothercust_ext where id_cust='
                                      + self.data_id_cust)
        self.data_dictionary['entrance'] = db.redo_and_check(data, 0)   # в словарь добавляется подъезд
        self.data_dictionary['floor'] = db.redo_and_check(data, 1)      # в словарь добавляется этаж
        self.data_dictionary['memo1'] = db.redo_and_check(data, 2)      # в словарь добавляется характеристики объекта

    def select_ops(self, db):
        data = db.requesting_data_one('select ops_type.title from ops,  ops_type '
                                      'where ops.type_ = ops_type.subtype_ and ops.id = ' + self.data_id_object)
        self.data_dictionary['type_ou'] = db.redo_and_check(data, 0)   # в словарь добавляется тип оконечного устройства

    def select_address2(self, db):
        command_sql = 'SELECT (select labels.label from  labels where addresses.id_street = labels.id  ), '\
                      ' addresses.house_num, addresses.building, addresses.korpus, addresses.flat_num, '\
                      ' (select labels.label from  labels where addresses.id_settl = labels.id  ) '\
                      ' FROM addresses where  addresses.id_owner=' + self.data_id_cust
        data = db.requesting_data_one(command_sql)
        # в словарь добавляется адрес объекта
        self.data_dictionary['address_object'] = db.address_format(data, 0, 1, 2, 3, 4, 5)

    def select_phones(self, db):
        data = db.requesting_data_one('select phone from phones where phone_type=1 and id_owner=' + self.data_id_cust)
        self.data_dictionary['phone'] = db.redo_and_check(data, 0)  # в словарь добавляется телефон объекта

    def select_xo_phones(self, db, line):
        data_phones_list = db.requesting_data_list('select phone_type, phone from phones where  id_owner='
                                                   + self.index_phone)
        phone_all = ''
        # в зависимости от типа data_phones[0] устанавливаем приставку с типом к телефону
        for data_phones in data_phones_list:
            if data_phones[0] == 1:
                phone_all += '  ' + db.redo_and_check(data_phones, 1) + '\n'
            if data_phones[0] == 3:
                phone_all += 'р.' + db.redo_and_check(data_phones, 1) + '\n'
            if data_phones[0] == 4:
                phone_all += 'c.' + db.redo_and_check(data_phones, 1) + '\n'
        self.data_dictionary['phone' + str(line)] = phone_all[:-1]  # удаляем последний символ

    def select_xo_name(self, db):
        # добавляем внутреннии select запросы для уменьшения кода и исключения ошибок при
        # неполном заполнение таблиц данными
        command_sql = 'SELECT xo.surname, xo.name, xo.patronymic, '\
                      '(select labels.label FROM labels where addresses.id_street = labels.id)'\
                      ', addresses.house_num,  addresses.building, addresses.korpus, addresses.flat_num, '\
                      'xo.comment, (select labels.label from  labels where addresses.id_settl = labels.id  ),'\
                      ' xo.id_xo FROM xo, addresses, anothercust_xo where addresses.id_owner=xo.id_xo '\
                      ' and anothercust_xo.id_xo =  xo.id_xo and anothercust_xo.id_cust =' + self.data_id_cust
        data_human = db.requesting_data_list(command_sql)
        line = 0
        for data in data_human:
            line += 1
            # словарь добавляется фамилия имя отческтво человека
            self.data_dictionary['name'+str(line)] = \
                db.redo_and_check(data, 0) + ' ' + db.redo_and_check(data, 1) + ' ' + db.redo_and_check(data, 2)
            # словарь добавляется комментарий по человеку
            self.data_dictionary['position'+str(line)] = db.redo_and_check(data, 8)
            # словарь добавляется адрес человека
            self.data_dictionary['address'+str(line)] = db.address_format(data, 3, 4, 5, 6, 7, 9)
            self.index_phone = db.redo_and_check(data, 10)
            if self.index_phone != 0:
                self.select_xo_phones(db, line)

    def select_object(self, db):
        command_sql = 'select objects.ncn, objects.label from objects where objects.isactive = 1 and  objects.parid =' \
                      + self.data_id_object
        data = db.requesting_data_list(command_sql)
        line = 0
        for cell in data:
            line += 1
            self.data_dictionary['Shn'+str(line)] = db.redo_and_check(cell, 0)    # номер шлейфа
            self.data_dictionary['Shm'+str(line)] = db.redo_and_check(cell, 1)    # описание шлейфа

    def read_data_fdb(self, path_db, card):
        db = SearchDb(path_db)
        if db.connect_db is not None:           # Есть коннект к базе данных
            if self.select_start(db, card):     # Есть в базе данных искомая карточка
                self.select_address(db)
                self.select_ops(db)
                self.select_address2(db)
                self.select_phones(db)
                self.select_xo_name(db)
                self.select_object(db)
                print('->карточка обработана')
                return True
        return False

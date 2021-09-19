__author__ = 'JaxsT'

from SearchDB import SearchDb


class WorkDbGdb:
    # data_type_object = ''
    data_dictionary = {}    # словарь для работы с процедурой
    data_id_name_object = ''
    id_key = ''
    id_type_otp = ''

    def select_start(self, db, card):
        # data_characteristic_object = ''
        command_sql = 'select cards.cr_key, cards.cr_oc_number, cards.cr_st_id, cards.cr_buildnum, ' \
                      'cards.cr_buildcorps, cards.cr_floor,cards.cr_entrance, cards.cr_placenum, ' \
                      'cards.cr_placedesc,cards.cr_safetyproblems, cards.cr_otp_id, cards.cr_buildfract, ' \
                      'cards.cr_crossphone, cards.cr_name, ' \
                      '(select str_name from  streets where streets.str_id = cards.cr_st_id )' \
                      ' from cards where cr_cardkey=' + card
        data = db.requesting_data_one(command_sql)
        if data is None:
            print('\033[1;31mERROR:Карточка [' + card + '] не найдена\033[0m')
            return False
        self.data_id_name_object = db.redo_and_check(data, 13)          # объект
        self.data_dictionary['card'] = card                             # в словарь добавляется позывной объекта
        self.data_dictionary['entrance'] = db.redo_and_check(data, 6)   # подъезд
        self.data_dictionary['floor'] = db.redo_and_check(data, 5)      # этаж
        self.data_dictionary['cont'] = db.redo_and_check(data, 1)       # номер договора
        self.data_dictionary['phone'] = db.redo_and_check(data, 12)     # телефон закроссированный
        self.id_key = db.redo_and_check(data, 0)                        # id - для определение типа прибора, список сотрудников, список шлейфов
        self.id_type_otp = db.redo_and_check(data, 10)                  # id - для определение типа объекта
        # характеристики объекта, уязвимости объекта
        self.data_dictionary['memo1'] = db.redo_and_check(data, 8) + '\n' + db.redo_and_check(data, 9)
        self.data_dictionary['address_object'] = db.address_format(data, 14, 3, 4, 11, 7)   # адрес объекта
        return True

    def select_otp_name(self, db):
        data_type_object = db.requesting_data_one('select otp_name from  objtypes where otp_id=' + self.id_type_otp)
        data_type_object = (db.redo_and_check(data_type_object, 0)).upper()
        self.data_dictionary['type_object'] = data_type_object
        if (data_type_object == 'КВАРТИРА') or (data_type_object == 'МХЛИГ'):
            # в словарь добавляется названание объекта для физического лица
            self.data_dictionary['type_object_physical'] = self.data_id_name_object
        else:
            # в словарь добавляется названание объекта для юридического лица
            self.data_dictionary['type_object_legal'] = self.data_id_name_object

    def select_xo(self, db):
        # создание списка с данными ФИО, статус, адрес, телефоны
        # Запрос на список сотрудников
        data_human = db.requesting_data_list('select * from  keymen where keymen.km_cr_key=' + self.id_key)
        line = 0
        for data in data_human:
            line += 1
            # в словарь добавляется ФИО сотрудника
            self.data_dictionary['name'+str(line)] = db.redo_and_check(data, 2) + ' ' + \
                                                     db.redo_and_check(data, 3) + ' ' + \
                                                     db.redo_and_check(data, 4)
            # в словарь добавляется комментарий по человеку
            self.data_dictionary['position'+str(line)] = db.redo_and_check(data, 9)
            self.data_dictionary['address'+str(line)] = db.redo_and_check(data, 7)   # в словарь добавляется адрес человека
            self.data_dictionary['phone'+str(line)] = db.redo_and_check(data, 8)     # в словарь добавляется телефон человека

    def select_uo(self, db):
        # создание списка с типом оконечного устройства
        data_ou = db.requesting_data_one('select uo.uo_name from  line, uo '
                                         'where uo.uo_ln_id = line.ln_id and line.ln_cr_key='+self.id_key)
        self.data_dictionary['type_ou'] = db.redo_and_check(data_ou, 0)      # определение оконечного устройства

    def select_objects(self, db):
        # Запрос на список шлейфов
        data = db.requesting_data_list('select sh_number,sh_name from  sh where sh.sh_cr_key=' + self.id_key)
        line = 0
        for cell in data:
            line += 1
            if str(cell[0]).isnumeric():
                self.data_dictionary['Shn'+str(line)] = str(cell[0]+1)  # номер шлейфа
            else:
                self.data_dictionary['Shn' + str(line)] = ''  # номер шлейфа
            self.data_dictionary['Shm'+str(line)] = db.redo_and_check(cell, 1)         # описание шлейфа

    def read_data_gdb(self, path_db, card):
        db = SearchDb(path_db)
        if db.connect_db is not None:           # Есть коннект к базе данных
            if self.select_start(db, card):     # Есть в базе данных искомая карточка
                self.select_otp_name(db)
                self.select_xo(db)
                self.select_objects(db)
                print('->карточка обработана')
                return True
        return False

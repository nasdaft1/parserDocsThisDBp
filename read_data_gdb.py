__author__ = 'JaxsT'

from SearchDB import connect_and_work_db
from SearchDB import redo_and_check

class work_db_gdb:
    #data_type_object = ''
    data_dictionary = {} # словарь для работы с процедурой
    def read_data_gdb(self,path_db, card):
        self.data_characteristic_object = ''
        db = connect_and_work_db(path_db)
        command_SQL = 'select cards.cr_key, cards.cr_oc_number, cards.cr_st_id, cards.cr_buildnum,cards.cr_buildcorps, ' \
                      'cards.cr_floor,cards.cr_entrance, cards.cr_placenum,cards.cr_placedesc,cards.cr_safetyproblems, '\
                      'cards.cr_otp_id,cards.cr_buildfract,cards.cr_crossphone, cards.cr_name, '\
                      '(select str_name from  streets where streets.str_id = cards.cr_st_id )'\
                      ' from cards where cr_cardkey=' +card
        data= db.requesting_data_one(command_SQL)
        data_id_name_object =  str(data[13]).rstrip() # объект
        #self.data_dictionary['ed']       = pult.upper()
        self.data_dictionary['card']     = card   #в словарь добавляется позывной объекта
        self.data_dictionary['entrance'] = str(data[6]) # подъезд
        self.data_dictionary['floor']    = str(data[5]) # этаж
        self.data_dictionary['cont']     = str(data[1]).rstrip() # номер договора
        self.data_dictionary['phone']    = str(data[12]).rstrip()# телефон закроссированный
        id_key         = str(data[0])   # id - для определение типа прибора, список сотрудников, список шлейфов
        id_address_object = str(data[2])# id - для определение адреса объекта
        id_type_otp    = str(data[10])  # id - для определение типа объекта
        data_type_object = db.requesting_data_one('select otp_name from  objtypes where otp_id=' + id_type_otp)
        data_type_object = (str(data_type_object[0]).rstrip()).upper()
        self.data_dictionary['type_object'] = data_type_object
        if (data_type_object == 'КВАРТИРА') or (data_type_object == 'МХЛИГ'):
            #в словарь добавляется названание объекта для физического лица
            self.data_dictionary['type_object_physical'] = data_id_name_object
        else:
            #в словарь добавляется названание объекта для юридического лица
            self.data_dictionary['type_object_legal'] = data_id_name_object
        street = db.requesting_data_one('select str_name from  streets where streets.str_id=' + id_address_object)
        self.data_dictionary['memo1']   = (str(data[8]) + '\n' + str(data[9])) #характеристики объекта, уязвимости объекта
        self.data_dictionary['address_object'] = db.address_format(data, 14, 3, 4, 11, 7) # адрес объекта
        #создание списка с типом оконечного устройства
        data = db.requesting_data_one('select uo.uo_name from  line, uo where uo.uo_ln_id = line.ln_id and line.ln_cr_key='+id_key)
        self.data_dictionary['type_ou'] = str(data[0]).rstrip() # определение оконечного устройства
        #создание списка с данными ФИО, статус, адрес, телефоны
        data_human = db.requesting_data_list('select * from  keymen where keymen.km_cr_key=' + id_key) #Запрос на список сотрудников
        line = 0
        for data in data_human:
            line+=1
            # в словарь добавляется ФИО сотрудника
            self.data_dictionary['name'+str(line)]     = str(data[2]).rstrip() +' '+ str(data[3]).rstrip() + ' ' + str(data[4]).rstrip()
            self.data_dictionary['position'+str(line)] = redo_and_check(data ,9) # в словарь добавляется комментарий по человеку
            self.data_dictionary['address'+str(line)]  = str(data[7]).rstrip()  # в словарь добавляется адрес человека
            self.data_dictionary['phone'+str(line)]  = str(data[8]).rstrip()  # в словарь добавляется телефон человека
        data = db.requesting_data_list('select sh_number,sh_name from  sh where sh.sh_cr_key=' + id_key) #Запрос на список шлейфов
        line = 0
        for cell in data:
            line+=1
            self.data_dictionary['Shn'+str(line)] = str(cell[0]+1) # номер шлейфа
            self.data_dictionary['Shm'+str(line)] = cell[1] # описание шлейфа

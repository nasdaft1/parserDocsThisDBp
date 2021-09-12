__author__ = 'JaxsT'

from read_data_fdb import work_db_fdb
from read_data_gdb import work_db_gdb
import os
from docxtpl import DocxTemplate

import datetime

class viev:
    original_docx_name =''
    def __init__(self,original_docx):
        self.original_docx_name = original_docx
        
    def viev_selection_(self,path_db,card, pult, directories):
        #path_os = str(os.path.abspath(os.curdir)) + '\\'
        path_os = ''
        path_db_type = path_db[-3:]
        if path_db_type == 'fdb' : # определение типа данных
            work_db = work_db_fdb()
            work_db.read_data_fdb(path_db,card)
        if path_db_type == 'gdb' :
            work_db = work_db_gdb()
            work_db.read_data_gdb(path_db,card)
        if (path_db_type == 'fdb') or (path_db_type == 'gdb'):
            context1= work_db.data_dictionary  # достаем из класса словарь
            now_time = datetime.datetime.now() # Текущая дата со временем
            context1['ed']   = pult.upper() # в словарь добавляем имя пульта
            context1['data'] = now_time.strftime("%d.%m.%y")+'.г' # в словарь добавляем дату
            if not os.path.isdir(directories): os.mkdir(directories) #если директория нету создается новый каталог
            doc = DocxTemplate(path_os+self.original_docx_name)
            doc.render(context1)
            path_and_name_file = directories + card + '.docx'
            print(path_and_name_file)
            try:
                doc.save(path_and_name_file)      # сохранить фаил word с данными
                os.system('start ' + path_and_name_file)  # открыть фаил word
            except:
                print('\033[1;31mERROR:Закройте фаил, фаил не смог изменится\033[0m')

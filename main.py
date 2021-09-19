__author__ = 'JaxsT'

from data_viev import Viev
import configparser
import os


def working_files(file_config, file_executive, original_docx):
    config = configparser.ConfigParser()
    try:
        config.read(file_config, encoding="utf-8")               # открытие файла конфигурации
        try:
            file = open(file_executive, 'r', encoding="utf-8")       # открытие файла исполнительного
            line_file = file.readlines()
            for line in line_file:
                sort_db = Viev(original_docx)
                text = line.replace('\n', '')           # убираем знак переноса строки
                text = text.replace(' ', '').upper()    # убираем лишнии пробелы и переводит в заглавные
                separator = text.find(',')              # поиск запятой в строке
                if separator != -1:                     # проверка на наличие зяпятой
                    pult = str(text[:separator])        # получаем позывной пульта
                    card = str(text[separator+1:])      # получекм номер карточки
                    try:
                        path_db = config[pult]['ip_path_db']
                        path_directories = 'resources/' + config[pult]['path_pult']
                        if card.isdigit():      # проверка для защиты от доступа к базе данных посторонними командами
                                                # дальнейшее выполнение допускается если card содержит только цифры
                            sort_db.viev_selection_(path_db, card, pult, path_directories)
                        else:
                            print('\033[1;31mERROR:номер пульта содержит посторонние знаки и символы [' + card + ']\033[0m')
                    except KeyError:
                        print('\033[1;31mERROR:неверный позывной пульта  [' + pult + '] отсутствует в config.ini\033[0m')
                else:
                    print('\033[1;31mERROR:строка не содержит запятой для разделения пульт, номер [' + text + ']\033[0m')
            file.close()
        except IOError:
            print('\033[1;31mERROR: ненайден ' + file_config + ' в каталоге ]\033[0m')
    except IOError:
        print('\033[1;31mERROR: ненайден ' + file_executive + ' в каталоге ]\033[0m')


def main():
    path = os.getcwd() + '\\resources\\'
    # фаил конфигурации, фаил исполнительный, фаил с оригиналом docx
    working_files(path + 'config.ini', path + 'command.txt', path + 'original.docx')


if __name__ == '__main__':
    main()

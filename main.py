__author__ = 'JaxsT'

from data_viev import viev
import configparser


def working_files(file_config, file_executive, original_docx):
    config = configparser.ConfigParser()
    config.read(file_config)               # открытие файла конфигурации
    file = open(file_executive, 'r')       # открытие файла исполнительного
    line_file = file.readlines()
    for line in line_file:
        sort_db = viev(original_docx)
        text = line.replace('\n', '')           # убираем знак переноса строки
        text = text.replace(' ', '').upper()    # убираем лишнии пробелы и переводит в заглавные
        separator = text.find(',')              # поиск запятой в строке
        if separator != -1:                     # проверка на наличие зяпятой
            pult = str(text[:separator])        # получаем позывной пульта
            card = str(text[separator+1:])      # получекм номер карточки
            try:
                path_db = config[pult]['ip_path_db']
                path_directories = config[pult]['path_pult']
                try:
                    x =int(card)    # проверка для защиты от доступа к базе данных посторонними командами
                    try:
                        sort_db.viev_selection_(path_db, card, pult, path_directories)
                        print(path_db + ',' + card)
                    except:
                        print('\033[1;31mERROR:не найдена в БД данные для карточке [' + text + ']\033[0m')
                except:
                    print('\033[1;31mERROR:номер пульта содержит посторонние знаки и символы [' + card + ']\033[0m')
            except:
                print('\033[1;31mERROR:неверный позывной пульта  [' + pult + '] отсутствует в config.ini\033[0m')
        else:
            print('\033[1;31mERROR:строка не содержит запятой для разделения пульт, номер [' + text + ']\033[0m')
    file.close()

def main():
    working_files('config.ini', 'command.txt', 'original.docx') # фаил конфигурации, фаил исполнительный, фаил с оригиналом

if __name__ == '__main__':
    main()

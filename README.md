Сокращение
ПО - проигранное обеспечение
СПИ -система передачи извещений
АРМ - автоматизированное рабочее место
БД – база данных

Создание программы для выборки данных из:
сервер (название УФА)  - БД FireBird ПО СПИ Приток-А
сервер (название ЗАРЯ) - БД FireBird ПО СПИ Приток-А
сервер (название Нева) - БД InterBase ПО СПИ Атлас(20)
сервер (название Дон)  - БД InterBase ПО СПИ Атлас(20)
и выгрузке данных в свободно модифицированный файл docx согласно полей, 
на основе отредактированного исполнительного файла.

Задачи:
-Проанализировать базы данных FireBird, InterBase ПО СПИ Приток-А, ПО СПИ Атлас(20) в каких таблицах и полях хранится информация:
	-Номер договора
	-Позывной
	-Номер пультовой
	-Название объекта
	-Телефон, задействованный для связи
	-Тип объекта
	-Адрес
	-подъезд
	-этаж
	-список ответственных лиц:
		-ФИО
		-должность
		-Адрес
		-Телефоны
	-блокировка объекта
	-шлейфа охраны:
		-номер шлейфа
		-наименование шлейфа
-Построить запросы для выгрузки данных из базы данных ПО СПИ Приток-А, ПО СПИ Атлас(20).
-Не встраивать запросы в саму базу данных, в связи с безопасностью, и ее работы 24ч в сутки, круглый год без выходных.
-Разрабатываемое ПО должно размещаться на АРМ системного администратора.
-Все сервера и АРМ системного администратора расположены в локальной сети без выхода во внешнюю сеть в целях безопасности.
-В графическом интерфейсе нет необходимости в связи с экономией ресурсов при разработке.
-Для указания команд по выгрузке данных с различных серверов и  использовать файл command.txt.
-Формат команд в command.txt должен содержать:
	позывной, пультовой номер
	Пример:
	заря, 2730
-Должен иметься у программы файл конфигурации config.ini в котором должны содержатся поля для настройки подключения
	-позывной для формирования команд в файле command.txt	
	-путь для подключения к серверу
	-путь куда сохранять файлы с выгружаемыми данными
	Пример:
	[НЕВА]		
	ip_path_db =192.168.2.101:/C:/DB/atlas.gdb 
	path_pult =НЕВА/ 
- ПО должно содержать файл original.docx  с полями, которые будут заполняться.
- Файл original.docx должен подлежать модификации, изменение будут, осуществляется согласно нормативным требованиям к 
оформлению документов. 
-Выгрузка данных должна осуществляется путем модификации original.docx и сохранение в папку с именем позывного и название 
файла соответствующему пультовому номеру. 
	Пример \ДОН\130.docx


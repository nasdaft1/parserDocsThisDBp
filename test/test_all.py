import unittest
from SearchDB import SearchDb


class MyTestCase(unittest.TestCase):
    @staticmethod
    # для автоматического тестирования результатов методов
    # подаваемые данные [тестиреый метод, аргумент для тестируемого метода, метод тестирования]
    # assertTrue, assertTrue, assertIsNone, assertIsNotNone
    def test_all(*resurs):  # универсальный тестировщик методов
        for index in resurs:
            name_funcion = index[0]  # присваеваем переменной класс с методом(фунцией)
            name_assert = index[2]
            result_funcion = name_funcion.__call__(index[1])  # запускаем тестируемый метод с атрибутами index[1]
            reply = f'\nТестируем:[{str(name_funcion.__module__)}.{str(name_funcion.__name__)}({index[1]})]' \
                    f'=[{result_funcion}],\n а должен быть получен[{str(index[2].__name__)}]'
            # запускаем индивидуальный тест из списка и вставляем результат фунции
            name_assert.__call__(result_funcion, reply)

    def test_all_list(self):
        resurs = [[SearchDb.test_connect_ip, '192.168.1.1', self.assertTrue],
                  [SearchDb.test_connect_ip, '192.168.2.2', self.assertFalse],
                  [SearchDb.test_connect_localhost_path, 'C:/DB/zaria.fdb', self.assertTrue],
                  [SearchDb.test_connect_localhost_path, 'F:/DB/zaria.fdb', self.assertFalse],
                  [SearchDb.checking_possible_connection, '192.168.2.101:/C:/DB/atlas.gdb', self.assertFalse],
                  [SearchDb.checking_possible_connection, 'localhost:/C:/DB/zaria.fdb', self.assertTrue],
                  [SearchDb('localhost:/C:/DB/zaria.fdb').requesting_data_one, 'Select * from 1', self.assertIsNone],
                  [SearchDb('localhost:/C:/DB/zaria.fdb').requesting_data_one, 'Select * from ANOTHERCUST', self.assertIsNotNone],
                  ]
        self.test_all(*resurs)

    def test1(self):
        self.assertEqual(SearchDb.redo_and_check((1, 'zx', 4), 0), '1')
        self.assertEqual(SearchDb.redo_and_check((1, 'zx', 4), 1), 'zx')
        self.assertEqual(SearchDb.redo_and_check((1, 'zx', 4), 2), '4')
        self.assertEqual(SearchDb.redo_and_check((1, None, 2), 1), '')
        self.assertEqual(SearchDb.redo_and_check((1, None, 2), 4), '')


if __name__ == '__main__':
    unittest.main()

import unittest

from SearchDB import SearchDb


class MyTestCase(unittest.TestCase):
    def test_connect_db(self):  # тест соединения с базой данных
        a = SearchDb('localhost:/C:/DB/zaria.fdb')
        b = a.requesting_data_one('Select * from ANOTHERCUST')
        # b = a.requesting_data_list('Select * from x')
        self.assertIsNotNone(b, 'w')

    def test_connect_db_error(self):  # тест соединения с базой данных
        a = SearchDb('localhost:/C:/DB/zaria.fdb')
        b = a.requesting_data_one('Select * from 1')
        self.assertIsNone(b)





    def test_connecting_localhost_path(self):
        result = SearchDb.test_connect_localhost_path('C:/DB/zaria.fdb')
        self.assertTrue(result)

    def test_connecting_localhost_path2(self):
        result = SearchDb.test_connect_localhost_path('F:/DB/zaria.fdb')
        self.assertFalse(result)

    def test_path_db(self):
        result = SearchDb.checking_possible_connection("192.168.2.101:/C:/DB/atlas.gdb")
        self.assertFalse(result)

    def test_path_db2(self):
        result = SearchDb.checking_possible_connection("localhost:/C:/DB/zaria.fdb")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()

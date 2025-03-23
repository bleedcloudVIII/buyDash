import unittest
from back.file_worker import FileWorker
import os

class TestFileWorker(unittest.TestCase):

    def test_empty_file(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "data", "empty.xlsx")
        fw = FileWorker(path)
        fw.file_read()

        data = fw.piechart_one_company(1, 2, "Google")
        self.assertEqual(data, {})

        data = fw.piechart_expense(1, 2)
        self.assertEqual(data, {})

        data = fw.table_for_company(1, 2, "Google")
        self.assertEqual(data, [])

        data = fw.table_for_companies(1, 2)
        self.assertEqual(data, [])

        data = fw.bar_chart(1, 2)
        self.assertEqual(data, {})

    def test_one_list_file(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "data", "one_list.xlsx")
        fw = FileWorker(path)
        fw.file_read()

        data = fw.piechart_one_company(1, 2, "Google")
        correct_data = {"Product1": 10, "Product2": 1}
        self.assertEqual(data, correct_data)

        data = fw.piechart_expense(1, 2)
        correct_data = {"Google": 60}
        self.assertEqual(data, correct_data)

        data = fw.table_for_company(1, 2, "Google")
        correct_data = [
            {
                "seller": "Seller1",
                "product": "Product1",
                "count": 10,
                "qty": 5,
                "all": 50,
                "unit": "шт."
            },
            {
                "seller": "Seller2",
                "product": "Product2",
                "count": 1,
                "qty": 10,
                "all": 10,
                "unit": "кг"
            }
        ]
        self.assertEqual(data, correct_data)

        data = fw.table_for_companies(1, 2)
        self.assertEqual(data, correct_data)

        data = fw.bar_chart(1, 2)
        correct_data = {"Google": {"Product1": 10, "Product2": 1}}
        self.assertEqual(data, correct_data)

    def test_bar_chart(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "data", "test_data.xlsx")
        fw = FileWorker(path)
        fw.file_read()

        data = fw.bar_chart(1, 1)
        correct_data = {
            "Google": {"Product1": 10, "Product2" : 1, "Product4": 665},
            "X": {"Product1": 10, "Product2": 2},
        }
        self.assertEqual(data, correct_data)

        data = fw.bar_chart(1, 2)
        correct_data = {
            "Google": {"Product1": 20, "Product2" : 2, "Product3": 1,"Product4": 665},
            "X": {"Product1": 20, "Product2": 3, "Product5": 1},
        }
        self.assertEqual(data, correct_data)

        data = fw.bar_chart(1, 3)
        correct_data = {
            "Google": {"Product1": 31, "Product2" : 2, "Product3": 13, "Product4": 665},
            "X": {"Product1": 20, "Product2": 3, "Product5": 1},
        }
        self.assertEqual(data, correct_data)

        data = fw.bar_chart(3, 3)
        correct_data = {
            "Google": {"Product1": 11, "Product3": 12}
        }
        self.assertEqual(data, correct_data)

    def test_pie_chart_one_company(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "data", "test_data.xlsx")
        fw = FileWorker(path)
        fw.file_read()
        
        data = fw.piechart_one_company(1, 2, "X")
        correct_data = {"Product1": 20, "Product2": 3, "Product5": 1}
        self.assertEqual(data, correct_data)
        
        data = fw.piechart_one_company(1, 1, "X")
        correct_data = {"Product1": 10, "Product2": 2}
        self.assertEqual(data, correct_data)

    def test_pie_chart(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "data", "test_data.xlsx")
        fw = FileWorker(path)
        fw.file_read()

        data = fw.piechart_expense(1, 1)
        correct_data = {"Google": 1390, "X": 70}
        self.assertEqual(data, correct_data)

        data = fw.piechart_expense(1, 2)
        correct_data = {"Google": 1462, "X": 142}
        self.assertEqual(data, correct_data)

        data = fw.piechart_expense(1, 3)
        correct_data = {"Google": 1642, "X": 142}
        self.assertEqual(data, correct_data)

    def test_table_one_company(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "data", "test_data.xlsx")
        fw = FileWorker(path)
        fw.file_read()

        data = fw.table_for_company(1, 1, "X")
        correct_data = [
            {
                "seller": "Seller1",
                "product": "Product1",
                "count": 10,
                "qty": 5,
                "all": 50,
                "unit": "шт."
            },
            {
                "seller": "Seller2",
                "product": "Product2",
                "count": 2,
                "qty": 10,
                "all": 20,
                "unit": "кг"
            }
        ]
        self.assertEqual(data, correct_data)

        data = fw.table_for_company(1, 2, "X")
        correct_data = [
            {
                "seller": "Seller1",
                "product": "Product1",
                "count": 20,
                "qty": 5,
                "all": 100,
                "unit": "шт."
            },
            {
                "seller": "Seller2",
                "product": "Product2",
                "count": 3,
                "qty": 10,
                "all": 30,
                "unit": "кг"
            },
            {
                "seller": "Seller3",
                "product": "Product5",
                "count": 1,
                "qty": 12,
                "all": 12,
                "unit": "кг"
            }
        ]
        self.assertEqual(data, correct_data)

    def test_table_all_company(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "data", "test_data.xlsx")
        fw = FileWorker(path)
        fw.file_read()

        data = fw.table_for_companies(1, 1)
        correct_data = [
            {
                "seller": "Seller1",
                "product": "Product1",
                "count": 20,
                "qty": 5,
                "all": 100,
                "unit": "шт."
            },
            {
                "seller": "Seller2",
                "product": "Product2",
                "count": 3,
                "qty": 10,
                "all": 30,
                "unit": "кг"
            },
            {
                "seller": "Seller3",
                "product": "Product4",
                "count": 665,
                "qty": 2,
                "all": 1330,
                "unit": "шт."
            }
        ]
        self.assertEqual(data, correct_data)

        data = fw.table_for_companies(1, 2)
        correct_data = [
            {
                "seller": "Seller1",
                "product": "Product1",
                "count": 40,
                "qty": 5,
                "all": 200,
                "unit": "шт."
            },
            {
                "seller": "Seller2",
                "product": "Product2",
                "count": 5,
                "qty": 10,
                "all": 50,
                "unit": "кг"
            },
            {
                "seller": "Seller3",
                "product": "Product4",
                "count": 665,
                "qty": 2,
                "all": 1330,
                "unit": "шт."
            },
            {
                "seller": "Seller3",
                "product": "Product3",
                "count": 1,
                "qty": 12,
                "all": 12,
                "unit": "кг"
            },
            {
                "seller": "Seller3",
                "product": "Product5",
                "count": 1,
                "qty": 12,
                "all": 12,
                "unit": "кг"
            }
        ]
        self.assertEqual(data, correct_data)
        
        data = fw.table_for_companies(1, 3)
        
        correct_data = [
            {
                "seller": "Seller1",
                "product": "Product1",
                "count": 50,
                "qty": 5,
                "all": 250,
                "unit": "шт."
            },
            {
                "seller": "Seller2",
                "product": "Product2",
                "count": 5,
                "qty": 10,
                "all": 50,
                "unit": "кг"
            },
            {
                "seller": "Seller3",
                "product": "Product4",
                "count": 665,
                "qty": 2,
                "all": 1330,
                "unit": "шт."
            },
            {
                "seller": "Seller3",
                "product": "Product3",
                "count": 1,
                "qty": 12,
                "all": 12,
                "unit": "кг"
            },
            {
                "seller": "Seller2",
                "product": "Product1",
                "count": 1,
                "qty": 10,
                "all": 10,
                "unit": "кг"
            },
            {
                "seller": "Seller2",
                "product": "Product3",
                "count": 12,
                "qty": 10,
                "all": 120,
                "unit": "кг"
            },
            {
                "seller": "Seller3",
                "product": "Product5",
                "count": 1,
                "qty": 12,
                "all": 12,
                "unit": "кг"
            }
        ]
        self.assertEqual(data, correct_data)
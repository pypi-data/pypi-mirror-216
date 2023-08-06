import unittest
from beancount.core import data
from src.importer import Importer
from beancount.ingest import cache
import datetime


class TestImporter(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_name(self):
        self.assertEqual(Importer(name="foo bar").name(), "foo bar")
        self.assertEqual(Importer().name(), "Generic yabci Importer")

    def test_identify(self):

        csv_file = cache._FileMemo("/home/bob/test.csv")
        json_file = cache._FileMemo("/home/bob/test.json")

        # no pattern
        importer = Importer()
        self.assertTrue(importer.identify(csv_file))
        self.assertTrue(importer.identify(json_file))

        # some pattern
        importer = Importer(file_pattern=".*\\.csv")
        self.assertTrue(importer.identify(csv_file))
        self.assertFalse(importer.identify(json_file))

    def test_is_duplicate(self):

        transaction = data.Transaction(
            {"id": "id_foo"},
            None,
            None,
            None,
            None,
            None,
            None,
            [],
        )

        transaction_bar = data.Transaction(
            {"id": "id_bar"},
            None,
            None,
            None,
            None,
            None,
            None,
            [],
        )

        self.assertTrue(Importer(duplication_key="meta.id").is_transaction_duplicate(transaction, [transaction]))
        self.assertFalse(Importer(duplication_key="meta.id").is_transaction_duplicate(transaction, [transaction_bar]))

    def test_map_transaction_no_mapping(self):
        importer = Importer()
        with self.assertRaises(Exception):
            importer.map_transaction({})

    def test_map_transaction(self):

        # case #1: no mapping passed
        importer = Importer()
        with self.assertRaises(Exception):
            importer.map_transaction({})

        # case #2: mapping passed
        importer = Importer(mapping_transaction={"date": "raw_date", "narration": "raw_desc"})

        transaction = importer.map_transaction({"raw_date": "2023-01-01T09:12:34", "raw_desc": "descriptino"})

        self.assertEqual(datetime.date(2023, 1, 1), transaction.date)
        self.assertIsInstance(transaction, data.Transaction)
        self.assertEqual("descriptino", transaction.narration)

    def test_get_transactions(self):
        importer = Importer(mapping_transactions="raw_transactions", mapping_transaction={"date": "raw_date"})

        # case #1: key not found in input data
        transactions = importer.get_transactions({"invalid": [{"raw_date": "2023-01-01T09:12:34"}]})
        with self.assertRaises(Exception):
            list(transactions)

        # case #2: found & mapped
        transactions = list(importer.get_transactions({"raw_transactions": [{"raw_date": "2023-01-01T09:12:34"}, {"raw_date": "2023-02-03T09:12:34"}]}))

        self.assertEqual(2, len(transactions))
        self.assertIsInstance(transactions[0], data.Transaction)
        self.assertEqual(datetime.date(2023, 1, 1), transactions[0].date)
        self.assertEqual(datetime.date(2023, 2, 3), transactions[1].date)

    def test_map_balance(self):

        # case #1: no mapping passed
        importer = Importer()
        with self.assertRaises(Exception):
            importer.map_balance({})

        # case #2: mapping passed
        importer = Importer(mapping_balance={"date": "raw_date"})

        balance = importer.map_balance({"raw_date": "2023-01-01T09:12:34"})

        self.assertIsInstance(balance, data.Balance)
        self.assertEqual(datetime.date(2023, 1, 1), balance.date)

    def test_get_balances(self):
        importer = Importer(mapping_balances="raw_balances", mapping_balance={"date": "raw_date"})

        # case #1: key not found in input data
        balances = importer.get_balances({"invalid": [{"raw_date": "2023-01-01T09:12:34"}]})
        with self.assertRaises(Exception):
            list(balances)

        # case #2: found & mapped
        balances = list(importer.get_balances({"raw_balances": [{"raw_date": "2023-01-01T09:12:34"}, {"raw_date": "2023-02-03T09:12:34"}]}))

        self.assertEqual(2, len(balances))
        self.assertIsInstance(balances[0], data.Balance)
        self.assertEqual(datetime.date(2023, 1, 1), balances[0].date)
        self.assertEqual(datetime.date(2023, 2, 3), balances[1].date)



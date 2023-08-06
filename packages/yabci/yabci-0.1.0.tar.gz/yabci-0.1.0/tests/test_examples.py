import os.path
import unittest
import yabci
from beancount.ingest import extract
import datetime
from beancount.core.data import Transaction, Posting
from beancount.core.amount import Amount
from decimal import Decimal
import subprocess


class TestQuery(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.path = None

    def _run_bean_extract(self, *args) -> str:
        cmd = ["bean-extract", *args]
        result = subprocess.run(cmd, cwd=self.path, stdout=subprocess.PIPE)

        # remove first two lines, since the contain the absolute path as comment
        # (which differs on each machine)
        plain_imported = "\n".join(result.stdout.decode('utf-8').split("\n")[2:]).strip()

        return plain_imported

    def _readfile(self, filename) -> str:
        fullpath = os.path.join(self.path, filename)
        return open(fullpath, "r").read().strip()

    def test_example_csv_basic(self):

        self.path = os.path.dirname(__file__) + "/../examples/csv-basic/"

        imported = self._run_bean_extract("config-csv-basic.py", "foo-bank-sample.csv")
        expected = self._readfile("expected-output.beancount")

        self.assertEqual(expected, imported)

    def test_example_csv_full(self):

        self.path = os.path.dirname(__file__) + "/../examples/csv-full/"

        imported = self._run_bean_extract(
            "-e",
            "existing.beancount",
            "config-csv-full.py",
            "venmo-sample.csv",
        )

        expected = self._readfile("expected-output.beancount")

        self.assertEqual(expected, imported)

    def test_example_android_moneywallet(self):

        self.path = os.path.dirname(__file__) + "/../examples/android-moneywallet/"

        imported = self._run_bean_extract(
            "-e",
            "existing.beancount",
            "config-android-moneywallet.py",
            "database.json",
        )

        expected = self._readfile("expected-output.beancount")

        self.assertEqual(expected, imported)

    def test_example_readme(self):

        self.path = os.path.dirname(__file__) + "/../examples/readme/"

        imported = self._run_bean_extract(
            "config.py",
            "sample.csv",
        )

        expected = self._readfile("expected-output.beancount")

        self.assertEqual(expected, imported)

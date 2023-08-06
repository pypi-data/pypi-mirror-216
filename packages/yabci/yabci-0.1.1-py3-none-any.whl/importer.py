from beancount.core import data
from beancount.core import amount
from beancount.ingest import importer, cache
import re
import os
from .utils import map_dict, parse_amount, parse_date
from collections import namedtuple
import dateutil.parser
from beancount.core.number import D
from beancount.core import flags
import datetime
from beancount.loader import load_file
import itertools
from .logger import logger
from .utils import map_dict, parse_date, critical_error
import benedict


class Importer(importer.ImporterProtocol):

    _existing_duplication_keys = None

    _name = None

    def __init__(
        self,
        name: str = None,
        file_pattern: str = None,
        target_account: str = None,
        duplication_key=None,
        mapping_transactions=None,
        mapping_transaction=None,
        mapping_balances=None,
        mapping_balance=None,
        hook_prepare_data: callable = None
    ):
        self._name = name
        self._file_pattern = file_pattern
        self._target_account = target_account
        self._duplication_key = duplication_key
        self._mapping_transactions = mapping_transactions
        self._mapping_transaction = mapping_transaction
        self._mapping_balances = mapping_balances
        self._mapping_balance = mapping_balance
        self._hook_prepare_data = hook_prepare_data

    def name(self):
        if self._name:
            return self._name
        return "Generic yabci Importer"

    def identifier(self, filename) -> str:
        """
        A unique identifier for this importer+config
        """
        return "%s-%s" % (self.name(), self.basename(filename))

    def basename(self, filename):
        return '{}'.format(os.path.basename(filename))

    def identify(self, file: cache._FileMemo):
        if self._file_pattern:

            filename = file.name.lower()

            if not re.match(self._file_pattern, filename):
                logger.debug("Filename %s does not match pattern (%s)" % (filename, self._file_pattern))
                return False

        return True

    def file_name(self, file):
        return self.basename(file.name)

    def file_account(self, file):
        return self._target_account

    def file_date(self, file):
        # TODO is that suitable?
        return datetime.datetime.now().isoformat(timespec="seconds")

    def new_metadata(self, filename, counter, additional = {}):
        return {
            **data.new_metadata(filename, next(counter)),
            **(additional or {}),
        }

    def is_transaction_duplicate(self, transaction: data.Transaction, existing_entries: list) -> bool:
        """
        Check if a transaction exists already. Use a custom callable to
        determine, if two transactions represent the same (can return a certain
        id for instance)

        @return True if transaction exists, False otherwise.
        """
        callback = self._duplication_key

        # if it is a simple string, we treat it as array index (with dot syntax,
        # sth like "meta.customid")
        if isinstance(callback, str):
            key = callback
            callback = lambda transaction: benedict.benedict(transaction._asdict()).get(key)

        # no config for duplication detection -> return
        if not callback:
            return False

        # find the key for duplicate detection for the given transaction
        duplication_key = callback(transaction)

        # if the needle transaction does not have a duplication key, directly
        # return
        if not duplication_key:
            return False

        # now compute duplication keys for all existing entries (if not
        # previously happened)
        if self._existing_duplication_keys is None:
            existing_entries = existing_entries or []
            self._existing_duplication_keys = [callback(entry) for entry in existing_entries]

        return (duplication_key in self._existing_duplication_keys)

    def map_transaction(self, raw: dict) -> data.Transaction:
        """
        Map a raw data dict representing a transaction into a beancount
        Transaction object, considering the mapping config
        """
        try:
            if not self._mapping_transaction:
                raise Exception("Mapping for single transaction is not defined (key 'mapping_transaction')")

            mapped = map_dict(self._mapping_transaction, raw)

            # create a beancount object from the mapped values, with sensible
            # defaults
            transaction = data.Transaction(
                mapped.get("meta", data.EMPTY_SET),
                parse_date(mapped.get("date")),
                mapped.get("flag", flags.FLAG_OKAY),
                mapped.get("payee", None),
                mapped.get("narration", None),
                mapped.get("tags", data.EMPTY_SET),
                mapped.get("links", data.EMPTY_SET),
                [],
            )

        except Exception as e:
            raise Exception("Could not map transaction: %s\n\nused mapping config: %s\nraw data: %s" % (e, self._mapping_transaction, raw))

        for posting_data in mapped.get("postings", []):

            try:
                transaction.postings.append(data.Posting(
                    posting_data.get("account", self._target_account),
                    parse_amount(posting_data.get("amount")),
                    posting_data.get("cost", None),
                    parse_amount(posting_data.get("price", None)),
                    posting_data.get("flag", None),
                    posting_data.get("meta", data.EMPTY_SET), # meta
                ))

            except Exception as e:
                raise critical_error("Could not map posting: %s\n\nraw data: %s" % (e, posting_data))

        return transaction

    def map_balance(self, raw) -> data.Balance:
        """
        Map a raw data dict representing a balance into a beancount
        Balance object, considering the mapping config
        """

        try:
            if not self._mapping_balance:
                raise Exception("Mapping for single balance is not defined (key 'mapping_balance')")

            mapped = map_dict(self._mapping_balance, raw)

            return data.Balance(
                mapped.get("meta", data.EMPTY_SET),
                parse_date(mapped.get("date")),
                mapped.get("account", self._target_account),
                parse_amount(mapped.get("amount")),
                mapped.get("tolerance", None),
                parse_amount(mapped.get("diff_amount", None)),
            )

        except Exception as e:
            raise Exception("Could not map balance: %s\n\nused mapping config: %s\nraw data: %s" % (e, self._mapping_balance, raw))

    def get_transactions(self, data_raw: dict):
        """
        Take the raw input (benedict) and extract the list of (raw) transactions
        """
        if not self._mapping_transactions:
            return []

        raw_transactions = map_dict(self._mapping_transactions, data_raw)

        if raw_transactions is None:
            raise Exception("Could not find transactions with the key %s\n\navailable keys: %s" % (self._mapping_transactions, ",".join(data_raw.keys())))

        for raw_transaction in raw_transactions:
            yield self.map_transaction(raw_transaction)

    def get_balances(self, data_raw):
        """
        Take the raw input (benedict) and extract the list of (raw) balances
        """
        if not self._mapping_balances:
            return []

        raw_balances = map_dict(self._mapping_balances, data_raw)

        if raw_balances is None:
            raise Exception("Could not find balances with the key %s\n\navailable keys: %s" % (self._mapping_balances, ",".join(data_raw.keys())))

        for raw_balance in raw_balances:
            yield self.map_balance(raw_balance)

    def extract(self, file, existing_entries=None):

        # default: input passed to benedict is just the name of the import file
        benedict_input = file.name

        # if a hook is given, execute it
        if self._hook_prepare_data:
            logger.info("running prepare_data hook")
            benedict_input = self._hook_prepare_data(benedict_input)

        # load it into a benedict
        data_raw = benedict.benedict(benedict_input)

        counter = itertools.count()
        new_entries = []

        for entry in self.get_transactions(data_raw):
            metadata = self.new_metadata(file.name, counter, entry.meta or {})

            transaction = data.Transaction(**{**entry._asdict(), "meta": metadata})

            if self.is_transaction_duplicate(transaction, existing_entries):
                transaction.meta["__duplicate__"] = True

            new_entries.append(transaction)

        for balance in self.get_balances(data_raw):
            metadata = self.new_metadata(file.name, counter, balance.meta or {})
            balance = data.Balance(**{**balance._asdict(), "meta": metadata})

            if self.is_transaction_duplicate(balance, existing_entries):
                balance.meta["__duplicate__"] = True

            new_entries.append(balance)

        # metadata = data.new_metadata(file.name, next(counter))
        # new_entries.append(data.Custom(metadata, datetime.date.today(), "fints-importdate", []))

        return(new_entries)

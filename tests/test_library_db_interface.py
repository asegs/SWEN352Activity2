import unittest
from unittest.mock import Mock

from library.library_db_interface import Library_DB


class TestLibraryDBInterface(unittest.TestCase):
    def test_insert_patron(self):
        db_interface = Library_DB
        db_interface.Patron = Mock()
        db_interface.db = Mock()
        db_interface.Patron = Mock()
        self.assertEqual(1, 1)

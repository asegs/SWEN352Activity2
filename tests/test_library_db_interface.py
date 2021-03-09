import unittest
from unittest.mock import Mock, patch

import library.library_db_interface
from library.patron import Patron
from library.library_db_interface import Library_DB


class TestLibraryDBInterface(unittest.TestCase):
    def test_insert_patron_not_patron(self):
        CuT = Library_DB
        self.assertEqual(None, CuT.insert_patron(CuT, 0))

    def test_insert_patron_mock_patron_not_in_db(self):
        mock_patron = Mock(Patron)
        mock_patron.get_memberid = Mock()
        mock_patron.get_memberid.return_value = ('1')

        CuT = Library_DB()
        CuT.close_db()
        CuT.db = Mock()
        CuT.db.search = Mock()
        CuT.db.search.return_value = None #patron is not in db
        CuT.db.insert = Mock()
        CuT.db.insert.return_value = 1

        CuT.insert_patron(mock_patron)

        CuT.db.insert.assert_called_once()  # patron is inserted if this happens

    def test_insert_patron_mock_patron_in_db(self):
        mock_patron = Mock(Patron)
        mock_patron.get_memberid = Mock()
        mock_patron.get_memberid.return_value = ('1')

        CuT = Library_DB()
        CuT.close_db()
        CuT.db = Mock()
        CuT.db.search = Mock()
        CuT.db.search.return_value = mock_patron  # patron is in db
        CuT.db.insert = Mock()
        CuT.db.insert.return_value = 1

        CuT.retrieve_patron = Mock()
        CuT.retrieve_patron.return_value = mock_patron #Can't subscript a mock so do this for now
        #and test retrieve_patron method later

        CuT.insert_patron(mock_patron)

        CuT.db.insert.assert_not_called()  # patron is not inserted because patron is in db

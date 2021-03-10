import unittest
from unittest.mock import Mock, patch

import os
import library.library_db_interface
from library.patron import Patron
from library.library_db_interface import Library_DB


class TestLibraryDBInterface(unittest.TestCase):
    CuT = Library_DB()
    CuT.close_db()
    def tearDown(self):
        if os.path.exists('db.json'):
            os.remove('db.json')
    def test_insert_patron_not_patron(self):
        self.assertEqual(None, self.CuT.insert_patron( 0))

    def test_insert_patron_mock_patron_not_in_db(self):
        mock_patron = Mock(Patron)
        mock_patron.get_memberid = Mock()
        mock_patron.get_memberid.return_value = ('1')
        self.CuT = Library_DB()
        self.CuT.close_db()
        self.CuT.db = Mock()
        self.CuT.db.search = Mock()
        self.CuT.db.search.return_value = None  # patron is not in db
        self.CuT.db.insert = Mock()
        self.CuT.db.insert.return_value = 1

        self.CuT.insert_patron(mock_patron)

        self.CuT.db.insert.assert_called_once()  # patron is inserted if this happens
    def test_insert_patron_mock_patron_in_db(self):
        mock_patron = Mock(Patron)
        mock_patron.get_memberid = Mock()
        mock_patron.get_memberid.return_value = ('1')
        self.CuT.db = Mock()
        self.CuT.db.search = Mock()
        self.CuT.db.search.return_value = mock_patron  # patron is in db
        self.CuT.db.insert = Mock()
        self.CuT.db.insert.return_value = 1

        self.CuT.retrieve_patron = Mock()
        self.CuT.retrieve_patron.return_value = mock_patron  # Can't subscript a mock so do this for now
        # and test retrieve_patron method later

        self.CuT.insert_patron(mock_patron)

        self.CuT.db.insert.assert_not_called()  # patron is not inserted because patron is in db

    def test_get_patron_count(self):
        self.CuT.db = Mock()
        self.CuT.db.all = Mock()
        self.CuT.db.all.return_value = []  # list of patrons in db
        self.assertEqual(0, self.CuT.get_patron_count())

    def test_get_patron_count_multiple(self):
        mock_patron = Mock(Patron)
        mock_patron.get_memberid = Mock()
        self.CuT.db = Mock()
        self.CuT.db.all = Mock()
        self.CuT.db.all.return_value = [mock_patron, mock_patron]  # list of patrons in db
        self.assertEqual(2, self.CuT.get_patron_count())

    def test_get_all_patrons(self):
        self.CuT.db = Mock()
        self.CuT.db.all = Mock()
        self.CuT.db.all.return_value = []  # list of patrons in db
        self.assertEqual([], self.CuT.get_all_patrons())

    def test_get_all_patrons_multiple(self):
        mock_patron = Mock(Patron)
        mock_patron.get_memberid = Mock()
        self.CuT.db = Mock()
        self.CuT.db.all = Mock()
        self.CuT.db.all.return_value = [mock_patron, mock_patron]  # list of patrons in db

        self.assertEqual([mock_patron, mock_patron], self.CuT.get_all_patrons())

    def test_update_patron_not_patron(self):
        self.assertEqual(None, self.CuT.update_patron(0))

    def test_update_patron(self):
        mock_patron = Mock(Patron)
        mock_patron.get_memberid = Mock()
        self.CuT.db = Mock()
        self.CuT.convert_patron_to_db_format = Mock()
        self.CuT.convert_patron_to_db_format.return_value = mock_patron
        self.CuT.db.update = Mock()

        self.CuT.update_patron(mock_patron)
        self.CuT.db.update.assert_called_once()

    def test_retrieve_patron(self):
        self.CuT = Library_DB()
        self.CuT.close_db()
        self.CuT.db = Mock()
        self.CuT.db.search = Mock()
        self.CuT.db.search.return_value = False
        self.assertEqual(None, self.CuT.retrieve_patron(1))

    def test_close_db(self):
        self.CuT.db = Mock()
        self.CuT.db.close = Mock()
        self.CuT.close_db()
        self.CuT.db.close.assert_called_once()

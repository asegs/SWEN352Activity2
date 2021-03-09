import unittest
from unittest.mock import Mock, patch
from library.ext_api_interface import *


class TestMakeRequest(unittest.TestCase):

    def setUp(self):
        self.books = Books_API()

    def test_make_successful_request(self):
        with patch('library.ext_api_interface.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            response = Books_API.make_request(self.books, "http://openlibrary.org/search.json")
            self.assertIsNotNone(response)

    def test_make_failed_request(self):
        with patch('library.ext_api_interface.requests.get') as mock_get:
            mock_get.return_value.status_code = 205
            response = Books_API.make_request(self.books, "http://openlibrary.org/search.json")
            self.assertIsNone(response)


class TestIsBookAvailable(unittest.TestCase):

    def setUp(self):
        self.books = Books_API()

    def test_book_is_available(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {'docs': [{'title': 'Redwall'}]}
            response = Books_API.is_book_available(self.books, 'Redwall')
            self.assertTrue(response)

    def test_book_is_unavailable(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {'docs': []}
            response = Books_API.is_book_available(self.books, 'Redwall')
            self.assertFalse(response)

    def test_no_response(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            response = Books_API.is_book_available(self.books, 'Redwall')
            self.assertFalse(response)


import unittest
from unittest.mock import Mock, patch
from library.ext_api_interface import *
import requests


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

    def test_connection_error(self):
        with patch('library.ext_api_interface.requests.get') as mock_get:
            mock_get.side_effect = requests.ConnectionError
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


class TestGetBooksByAuthor(unittest.TestCase):
    def setUp(self):
        self.books = Books_API()

    def test_valid_author_one_book(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {'docs': [{'title_suggest': 'Redwall'}]}
            response = Books_API.books_by_author(self.books, "Brian Jacques")
            self.assertEqual(1, len(response))

    def test_valid_author_three_books(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'title_suggest': 'Redwall'}, {'title_suggest': 'Cornflower'}, {'title_suggest': 'Martin'}]}
            response = Books_API.books_by_author(self.books, 'Brian Jacques')
            self.assertEqual(3, len(response))

    def test_valid_author_correct_title(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'title_suggest': 'Redwall'}]}
            response = Books_API.books_by_author(self.books, 'Brian Jacques')
            self.assertEqual('Redwall', response[0])

    def test_no_books_found_still_docs(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': []}
            response = Books_API.books_by_author(self.books, "Brian Jacques")
            self.assertEqual(0, len(response))

    def test_no_books_found_no_data(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = False
            response = Books_API.books_by_author(self.books, "Brian Jacques")
            self.assertEqual(0, len(response))


class TestGetBookInfo(unittest.TestCase):
    def setUp(self):
        self.books = Books_API()

    def test_get_book_info_all_data(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'title': 'Redwall', 'publisher': 'Philomel', 'publish_year': 1986, 'language': 'English'}]}
            expected_book = {'title': 'Redwall', 'publisher': 'Philomel', 'publish_year': 1986, 'language': 'English'}
            response = Books_API.get_book_info(self.books, "Redwall")
            self.assertEqual(expected_book, response[0])

    def test_get_book_info_no_publisher(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'title': 'Redwall', 'publish_year': 1986, 'language': 'English'}]}
            expected_book = {'title': 'Redwall', 'publish_year': 1986, 'language': 'English'}
            response = Books_API.get_book_info(self.books, "Redwall")
            self.assertEqual(expected_book, response[0])

    def test_get_book_info_no_year(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'title': 'Redwall', 'publisher': 'Philomel', 'language': 'English'}]}
            expected_book = {'title': 'Redwall', 'publisher': 'Philomel', 'language': 'English'}
            response = Books_API.get_book_info(self.books, "Redwall")
            self.assertEqual(expected_book, response[0])

    def test_get_book_info_no_language(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'title': 'Redwall', 'publisher': 'Philomel', 'publish_year': 1986}]}
            expected_book = {'title': 'Redwall', 'publisher': 'Philomel', 'publish_year': 1986}
            response = Books_API.get_book_info(self.books, "Redwall")
            self.assertEqual(expected_book, response[0])

    def test_get_book_info_minimal_data(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'title': 'Redwall'}]}
            expected_book = {'title': 'Redwall'}
            response = Books_API.get_book_info(self.books, "Redwall")
            self.assertEqual(expected_book, response[0])

    def test_get_book_info_no_data_still_docs(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': []}
            response = Books_API.get_book_info(self.books, "Redwall")
            self.assertEqual(0, len(response))

    def test_get_book_info_two_books(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'title': 'Redwall', 'publisher': 'Philomel', 'publish_year': 1986, 'language': 'English'},
                         {'title': 'Cornflower'}]}
            expected_books = [
                {'title': 'Redwall', 'publisher': 'Philomel', 'publish_year': 1986, 'language': 'English'},
                {'title': 'Cornflower'}]
            response = Books_API.get_book_info(self.books, "Redwall")
            self.assertEqual(expected_books, response)

    def test_get_book_info_no_data(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = False
            response = Books_API.get_book_info(self.books, "Redwall")
            self.assertEqual(0,len(response))



class TestGetEbooks(unittest.TestCase):
    def setUp(self):
        self.books = Books_API()

    def test_get_ebook_normal(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'ebook_count_i': 1, 'title': 'Redwall'}]}
            expected_ebook = {'ebook_count': 1, 'title': 'Redwall'}
            response = Books_API.get_ebooks(self.books, "Redwall")
            self.assertEqual(expected_ebook, response[0])

    def test_get_ebook_count_zero(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'ebook_count_i': 0, 'title': 'Redwall'}]}
            response =  Books_API.get_ebooks(self.books,"Redwall")
            self.assertEqual(0,len(response))

    def test_get_ebook_no_data(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = False
            response = Books_API.get_ebooks(self.books, "Redwall")
            self.assertEqual(0,len(response))

    def test_get_ebooks_two(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'ebook_count_i': 1, 'title': 'Redwall'},{'ebook_count_i':5,'title':'Cornflower'}]}
            expected_ebooks = [{'ebook_count': 1, 'title': 'Redwall'},{'ebook_count':5,'title':'Cornflower'}]
            response = Books_API.get_ebooks(self.books, "Redwall")
            self.assertEqual(expected_ebooks, response)

    def test_get_ebooks_three_one_fail(self):
        with patch('library.ext_api_interface.Books_API.make_request') as mock_get:
            mock_get.return_value = {
                'docs': [{'ebook_count_i': 1, 'title': 'Redwall'},{'ebook_count_i':5,'title':'Cornflower'},{'title':'Mossflower','ebook_count_i':0}]}
            expected_ebooks = [{'ebook_count': 1, 'title': 'Redwall'},{'ebook_count':5,'title':'Cornflower'}]
            response = Books_API.get_ebooks(self.books, "Redwall")
            self.assertEqual(expected_ebooks, response)

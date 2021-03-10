import unittest
from unittest import TestCase
from unittest.mock import Mock
import os.path
from os import path
from library.library import Library
from library.library_db_interface import Library_DB
from library.ext_api_interface import Books_API
from library.patron import Patron

dummy_book_list_json = [
    {
        'title': 'Adventures of Elvis',
        'ebook_count': 2
    },
    {
        'title': 'Elvis is Here',
        'ebook_count': 4
    },
    {
        'title': 'You cant handle the truth',
        'ebook_count': 1
    },
    {
        'title': 'It is me or you',
        'ebook_count': 0
    },
]

dummy_similar_book_list_json = [
    {
        'title': 'Adventures of Elvis',
        'ebook_count': 2
    },
    {
        'title': 'Elvis is Here',
        'ebook_count': 4
    },
    {
        'title': 'Adventure time',
        'ebook_count': 1
    },
    {
        'title': 'Adventures of Alibaba',
        'ebook_count': 3
    },
]

dummy_author_book_list_json = [
    'Adventures of Elvis',
    'Meet me now',
    'Hello, you again?'
]

book_language_list = [
    {
        'language': ['eng']
    },
    {
        'language': ['fre']
    },
    {
        'language': ['hindi']
    },
    {
        'language': ['lit']
    },
    {
        'language': ['spa']
    },
]


class TestLibrary(TestCase):

    def setUp(self) -> None:
        self.CuT = Library()
        self.patron = Mock()
        self.book_title_there = 'Adventures of Elvis'
        self.book_title_not_there = 'Adventures of Dino'
        self.book_title_language = 'Harry Potter'
        self.book_author = 'Dummy Name'
        self.first_name = 'Sam'
        self.last_name = 'Wheeler'
        self.age = 27
        self.member_id = 100001

    def test_library_db_created(self):
        # Assert
        self.assertIsInstance(self.CuT.db, Library_DB)

    def test_book_api_created(self):
        # Assert
        self.assertIsInstance(self.CuT.api, Books_API)

    def test_book_is_ebook(self):
        # Action
        self.CuT.api = Mock()
        self.CuT.api.get_ebooks.return_value = dummy_book_list_json

        # Assert
        self.assertTrue(self.CuT.is_ebook(self.book_title_there))

    def test_book_is_not_ebook(self):
        # Action
        self.CuT.api = Mock()
        self.CuT.api.get_ebooks.return_value = dummy_book_list_json

        # Assert
        self.assertFalse(self.CuT.is_ebook(self.book_title_not_there))

    def test_gets_book_count_for_more_than_zero(self):

        # Action
        self.CuT.api = Mock()
        self.CuT.api.get_ebooks.return_value = dummy_similar_book_list_json

        # Assert
        self.assertEqual(self.CuT.get_ebooks_count(self.book_title_there), 10)

    def test_gets_book_count_for_zero_books(self):

        # Action
        self.CuT.api = Mock()
        self.CuT.api.get_ebooks.return_value = []

        # Assert
        self.assertEqual(self.CuT.get_ebooks_count(self.book_title_not_there), 0)

    def test_gets_book_count_if_no_book_is_there(self):

        # Action
        self.CuT.api = Mock()
        self.CuT.api.get_ebooks.return_value = [
            {
                'title': 'Adventures of Dino',
                'ebook_count': 0
            },
        ]

        # Assert
        self.assertEqual(self.CuT.get_ebooks_count(self.book_title_not_there), 0)

    def test_author_entered_for_book_is_true(self):

        # Action
        self.CuT.api = Mock()
        self.CuT.api.books_by_author.return_value = dummy_author_book_list_json

        # Assert
        self.assertTrue(self.CuT.is_book_by_author(self.book_author, self.book_title_there))

    def test_author_entered_for_book_is_false(self):

        # Action
        self.CuT.api = Mock()
        self.CuT.api.books_by_author.return_value = dummy_author_book_list_json

        # Assert
        self.assertFalse(self.CuT.is_book_by_author(self.book_author, self.book_title_not_there))

    def test_author_entered_for_book_has_no_book_in_library(self):

        # Action
        self.CuT.api = Mock()
        self.CuT.api.books_by_author.return_value = []

        # Assert
        self.assertFalse(self.CuT.is_book_by_author(self.book_author, self.book_title_not_there))

    def test_gets_languages_for_the_book(self):

        # Action
        self.CuT.api = Mock()
        self.CuT.api.get_book_info.return_value = book_language_list
        languages = self.CuT.get_languages_for_book(self.book_title_language)

        # Assert
        self.assertEqual(len(languages), len(book_language_list))

    def test_gets_one_language_for_the_book(self):

        language_list = [
            {
                'language': ['eng']
            }
        ]

        # Action
        self.CuT.api = Mock()
        self.CuT.api.get_book_info.return_value = language_list
        languages = self.CuT.get_languages_for_book(self.book_title_language)

        # Assert
        self.assertEqual(len(languages), 1)

    def test_gets_zero_language_for_no_book(self):

        # Assume
        language_list = []

        # Action
        self.CuT.api = Mock()
        self.CuT.api.get_book_info.return_value = language_list
        languages = self.CuT.get_languages_for_book(self.book_title_language)

        # Assert
        self.assertEqual(len(languages), 0)

    def test_gets_the_correct_languages_for_the_book(self):

        # Action
        self.CuT.api = Mock()
        self.CuT.api.get_book_info.return_value = book_language_list
        languages = self.CuT.get_languages_for_book(self.book_title_language)
        all_languages = list()
        for ebook in book_language_list:
            all_languages.append(ebook['language'][0])
        is_same = True
        for lang in languages:
            if lang not in all_languages:
                is_same = False
                break

        # Assert
        self.assertTrue(is_same)

    def test_patron_is_registered_in_db(self):

        # Assume
        self.CuT.db = Mock()
        self.CuT.db.insert_patron.return_value = 1
        self.CuT.db.retrieve_patron.return_value = True
        patron = Patron(self.first_name, self.last_name, self.age, self.member_id)
        patron.get_memberID = Mock(return_value=1)

        # Action
        self.CuT.register_patron(self.first_name, self.last_name, self.age, self.member_id)
        is_patron_registered = self.CuT.is_patron_registered(patron)
        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertTrue(is_patron_registered)

    def test_patron_is_not_registered_in_db(self):

        # Assume
        self.CuT.db = Mock()
        self.CuT.db.insert_patron.return_value = 1
        self.CuT.db.retrieve_patron.return_value = False
        patron = Patron(self.first_name, self.last_name, self.age, self.member_id)
        patron.get_memberID = Mock(return_value=1)

        # Action
        self.CuT.register_patron(self.first_name, self.last_name, self.age, self.member_id)
        is_patron_registered = self.CuT.is_patron_registered(patron)
        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertFalse(is_patron_registered)

    def test_has_patron_borrowed_book_true(self):

        # Assume
        self.CuT.db = Mock()

        self.patron.fname.return_value = self.first_name
        self.patron.lname.return_value = self.last_name
        self.patron.age.return_value = self.age
        self.patron.memberID.return_value = self.member_id
        self.patron.borrowed_books.return_value = []
        self.CuT.db.update_patron.return_value = True
        self.patron.add_borrowed_book.return_value = True
        self.patron.get_borrowed_books.return_value = [
            self.book_title_there.lower()
        ]

        # Action
        self.CuT.borrow_book(self.book_title_there, self.patron)
        is_book_borrowed = self.CuT.is_book_borrowed(self.book_title_there, self.patron)

        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertTrue(is_book_borrowed)

    def test_has_patron_borrowed_book_false(self):

        # Assume
        self.CuT.db = Mock()

        self.patron.fname.return_value = self.first_name
        self.patron.lname.return_value = self.last_name
        self.patron.age.return_value = self.age
        self.patron.memberID.return_value = self.member_id
        self.patron.borrowed_books.return_value = []
        self.CuT.db.update_patron.return_value = True
        self.patron.add_borrowed_book.return_value = True
        self.patron.get_borrowed_books.return_value = [
            'Some other book title'
        ]

        # Action
        self.CuT.borrow_book(self.book_title_there, self.patron)
        is_book_borrowed = self.CuT.is_book_borrowed(self.book_title_there, self.patron)

        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertFalse(is_book_borrowed)

    def test_patron_has_returned_book(self):

        # Assume
        self.CuT.db = Mock()

        self.patron.fname.return_value = self.first_name
        self.patron.lname.return_value = self.last_name
        self.patron.age.return_value = self.age
        self.patron.memberID.return_value = self.member_id
        self.patron.borrowed_books.return_value = [
            self.book_title_there.lower()
        ]
        self.CuT.db.update_patron.return_value = True
        self.patron.return_borrowed_book.return_value = True
        self.patron.get_borrowed_books.return_value = []

        # Action
        self.CuT.borrow_book(self.book_title_there, self.patron)
        self.CuT.return_borrowed_book(self.book_title_there, self.patron)
        is_book_borrowed = self.CuT.is_book_borrowed(self.book_title_there, self.patron)

        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertFalse(is_book_borrowed)


if __name__ == '__main__':
    unittest.main()

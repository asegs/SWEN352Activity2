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
    'Adventures of life',
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

    def test_library_db_created(self):
        # Action
        CuT = Library()
        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertIsInstance(CuT.db, Library_DB)

    def test_book_api_created(self):
        # Action
        CuT = Library()
        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertIsInstance(CuT.api, Books_API)

    def test_book_is_ebook(self):
        # Assume
        book_title = 'Adventures of Elvis'

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.get_ebooks.return_value = dummy_book_list_json

        # Assert
        self.assertTrue(CuT.is_ebook(book_title))

    def test_book_is_not_ebook(self):
        # Assume
        book_title = 'Adventures of Dino'

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.get_ebooks.return_value = dummy_book_list_json

        # Assert
        self.assertFalse(CuT.is_ebook(book_title))

    def test_gets_book_count_for_more_than_zero(self):
        # Assume
        book_title = 'Adventures of Elvis'

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.get_ebooks.return_value = dummy_similar_book_list_json

        # Assert
        self.assertEqual(CuT.get_ebooks_count(book_title), 10)

    def test_gets_book_count_for_zero_books(self):
        # Assume
        book_title = 'It is me or you'

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.get_ebooks.return_value = []

        # Assert
        self.assertEqual(CuT.get_ebooks_count(book_title), 0)

    def test_gets_book_count_if_no_book_is_there(self):
        # Assume
        book_title = 'Adventures of Dino'

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.get_ebooks.return_value = [
            {
                'title': 'Adventures of Dino',
                'ebook_count': 0
            },
        ]

        # Assert
        self.assertEqual(CuT.get_ebooks_count(book_title), 0)

    def test_author_entered_for_book_is_true(self):
        # Assume
        book_title = 'Adventures of life'
        book_author = 'Dummy Name'

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.books_by_author.return_value = dummy_author_book_list_json

        # Assert
        self.assertTrue(CuT.is_book_by_author(book_author, book_title))

    def test_author_entered_for_book_is_false(self):
        # Assume
        book_title = 'Adventures of life?'
        book_author = 'Dummy Name'

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.books_by_author.return_value = dummy_author_book_list_json

        # Assert
        self.assertFalse(CuT.is_book_by_author(book_author, book_title))

    def test_author_entered_for_book_has_no_book_in_library(self):
        # Assume
        book_title = 'Adventures of life'
        book_author = 'Dummy Name'

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.books_by_author.return_value = []

        # Assert
        self.assertFalse(CuT.is_book_by_author(book_author, book_title))

    def test_gets_languages_for_the_book(self):
        # Assume
        book_title = 'Harry Potter'

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.get_book_info.return_value = book_language_list
        languages = CuT.get_languages_for_book(book_title)

        # Assert
        self.assertEqual(len(languages), len(book_language_list))

    def test_gets_one_language_for_the_book(self):
        # Assume
        book_title = 'Harry Potter'
        language_list = [
            {
                'language': ['eng']
            }
        ]

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.get_book_info.return_value = language_list
        languages = CuT.get_languages_for_book(book_title)

        # Assert
        self.assertEqual(len(languages), 1)

    def test_gets_zero_language_for_no_book(self):
        # Assume
        book_title = 'Harry Potter'
        language_list = []

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.get_book_info.return_value = language_list
        languages = CuT.get_languages_for_book(book_title)

        # Assert
        self.assertEqual(len(languages), 0)

    def test_gets_the_correct_languages_for_the_book(self):
        # Assume
        book_title = 'Harry Potter'

        # Action
        CuT = Library()
        CuT.api = Mock()
        CuT.api.get_book_info.return_value = book_language_list
        languages = CuT.get_languages_for_book(book_title)
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
        first_name = 'Sam'
        last_name = 'Wheeler'
        age = 27
        member_id = 100001
        CuT = Library()
        CuT.db = Mock()
        CuT.db.insert_patron.return_value = 1
        CuT.db.retrieve_patron.return_value = True
        patron = Patron(first_name, last_name, age, member_id)
        patron.get_memberID = Mock(return_value=1)

        # Action
        patron = Patron(first_name, last_name, age, member_id)
        CuT.register_patron(first_name, last_name, age, member_id)
        is_patron_registered = CuT.is_patron_registered(patron)
        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertTrue(is_patron_registered)

    def test_patron_is_not_registered_in_db(self):
        # Assume
        first_name = 'Sam'
        last_name = 'Wheeler'
        age = 27
        member_id = 100001
        CuT = Library()
        CuT.db = Mock()
        CuT.db.insert_patron.return_value = 1
        CuT.db.retrieve_patron.return_value = False
        patron = Patron(first_name, last_name, age, member_id)
        patron.get_memberID = Mock(return_value=1)

        # Action
        patron = Patron(first_name, last_name, age, member_id)
        CuT.register_patron(first_name, last_name, age, member_id)
        is_patron_registered = CuT.is_patron_registered(patron)
        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertFalse(is_patron_registered)

    def test_has_patron_borrowed_book_true(self):
        # Assume
        first_name = 'Sam'
        last_name = 'Wheeler'
        age = 27
        member_id = 100001
        book_title = 'Adventures of Tintin'

        CuT = Library()
        CuT.db = Mock()
        patron = Mock()

        patron.fname.return_value = first_name
        patron.lname.return_value = last_name
        patron.age.return_value = age
        patron.memberID.return_value = member_id
        patron.borrowed_books.return_value = []
        CuT.db.update_patron.return_value = True
        patron.add_borrowed_book.return_value = True
        patron.get_borrowed_books.return_value = [
            book_title.lower()
        ]

        # Action
        CuT.borrow_book(book_title, patron)
        is_book_borrowed = CuT.is_book_borrowed(book_title, patron)

        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertTrue(is_book_borrowed)

    def test_has_patron_borrowed_book_false(self):
        # Assume
        first_name = 'Sam'
        last_name = 'Wheeler'
        age = 27
        member_id = 100001
        book_title = 'Adventures of Adam'

        CuT = Library()
        CuT.db = Mock()
        patron = Mock()

        patron.fname.return_value = first_name
        patron.lname.return_value = last_name
        patron.age.return_value = age
        patron.memberID.return_value = member_id
        patron.borrowed_books.return_value = []
        CuT.db.update_patron.return_value = True
        patron.add_borrowed_book.return_value = True
        patron.get_borrowed_books.return_value = [
            'Some other book title'
        ]

        # Action
        CuT.borrow_book(book_title, patron)
        is_book_borrowed = CuT.is_book_borrowed(book_title, patron)

        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertFalse(is_book_borrowed)

    def test_patron_has_returned_book(self):
        # Assume
        first_name = 'Sam'
        last_name = 'Wheeler'
        age = 27
        member_id = 100001
        book_title = 'Adventures of Tintin'

        CuT = Library()
        CuT.db = Mock()
        patron = Mock()

        patron.fname.return_value = first_name
        patron.lname.return_value = last_name
        patron.age.return_value = age
        patron.memberID.return_value = member_id
        patron.borrowed_books.return_value = [
            book_title.lower()
        ]
        CuT.db.update_patron.return_value = True
        patron.return_borrowed_book.return_value = True
        patron.get_borrowed_books.return_value = []

        # Action
        CuT.borrow_book(book_title, patron)
        CuT.return_borrowed_book(book_title, patron)
        is_book_borrowed = CuT.is_book_borrowed(book_title, patron)

        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertFalse(is_book_borrowed)


if __name__ == '__main__':
    unittest.main()

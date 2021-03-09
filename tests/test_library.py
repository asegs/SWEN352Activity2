from unittest import TestCase
from unittest.mock import Mock
import os.path
from os import path

from library.library import Library
from library.library_db_interface import Library_DB
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

    def test_constructor_works_as_intended(self):
        # Assume

        # Action

        # Assert

        pass

    def test_book_is_ebook(self):
        # Assume
        book_title = 'Adventures of Elvis'

        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.get_ebooks.return_value = dummy_book_list_json

        # Assert
        self.assertTrue(lib_obj.is_ebook(book_title))

    def test_book_is_not_ebook(self):
        # Assume
        book_title = 'Adventures of Dino'

        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.get_ebooks.return_value = dummy_book_list_json

        # Assert
        self.assertFalse(lib_obj.is_ebook(book_title))

    def test_gets_book_count_for_more_than_zero(self):
        # Assume
        book_title = 'Adventures of Elvis'

        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.get_ebooks.return_value = dummy_similar_book_list_json

        # Assert
        self.assertEqual(lib_obj.get_ebooks_count(book_title), 10)

    def test_gets_book_count_for_zero_books(self):
        # Assume
        book_title = 'It is me or you'

        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.get_ebooks.return_value = []

        # Assert
        self.assertEqual(lib_obj.get_ebooks_count(book_title), 0)

    def test_gets_book_count_if_no_book_is_there(self):
        # Assume
        book_title = 'Adventures of Dino'

        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.get_ebooks.return_value = [
            {
                'title': 'Adventures of Dino',
                'ebook_count': 0
            },
        ]

        # Assert
        self.assertEqual(lib_obj.get_ebooks_count(book_title), 0)

    def test_author_entered_for_book_is_true(self):
        # Assume
        book_title = 'Adventures of life'
        book_author = 'Dummy Name'

        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.books_by_author.return_value = dummy_author_book_list_json

        # Assert
        self.assertTrue(lib_obj.is_book_by_author(book_author, book_title))

    def test_author_entered_for_book_is_false(self):
        # Assume
        book_title = 'Adventures of life?'
        book_author = 'Dummy Name'

        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.books_by_author.return_value = dummy_author_book_list_json

        # Assert
        self.assertFalse(lib_obj.is_book_by_author(book_author, book_title))

    def test_author_entered_for_book_has_no_book_in_library(self):
        # Assume
        book_title = 'Adventures of life'
        book_author = 'Dummy Name'

        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.books_by_author.return_value = []

        # Assert
        self.assertFalse(lib_obj.is_book_by_author(book_author, book_title))

    def test_gets_languages_for_the_book(self):
        # Assume
        book_title = 'Harry Potter'

        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.get_book_info.return_value = book_language_list
        languages = lib_obj.get_languages_for_book(book_title)

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
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.get_book_info.return_value = language_list
        languages = lib_obj.get_languages_for_book(book_title)

        # Assert
        self.assertEqual(len(languages), 1)

    def test_gets_zero_language_for_no_book(self):
        # Assume
        book_title = 'Harry Potter'
        language_list = []

        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.get_book_info.return_value = language_list
        languages = lib_obj.get_languages_for_book(book_title)

        # Assert
        self.assertEqual(len(languages), 0)

    def test_gets_the_correct_languages_for_the_book(self):
        # Assume
        book_title = 'Harry Potter'

        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.get_book_info.return_value = book_language_list
        languages = lib_obj.get_languages_for_book(book_title)
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

    def test_db_storage_is_0_when_created(self):
        # Assume
        db_obj = Library_DB()
        # Action
        storage_count = db_obj.get_patron_count()
        # Assert

        self.assertEqual(storage_count, 0)

    def test_patron_added_to_library_db(self):
        # Assume
        first_name = 'Sam'
        last_name = 'Wheeler'
        age = 27
        member_id = 100001

        # Action
        lib_obj = Library()
        lib_obj.db.get_patron_count()
        lib_obj.register_patron(first_name, last_name, age, member_id)
        storage_count = lib_obj.db.get_patron_count()
        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertEqual(storage_count, 1)

    def test_patron_exists_in_library_db(self):
        # Assume
        first_name = 'Sam'
        last_name = 'Wheeler'
        age = 27
        member_id = 100001

        # Action
        lib_obj = Library()
        lib_obj.db.get_patron_count()
        id = lib_obj.register_patron(first_name, last_name, age, member_id)
        id = lib_obj.register_patron(first_name, last_name, age, member_id)
        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertEqual(None, id)

    def test_patron_is_registered_in_db(self):
        # Assume
        first_name = 'Sam'
        last_name = 'Wheeler'
        age = 27
        member_id = 100001

        # Action
        lib_obj = Library()
        lib_obj.db.get_patron_count()
        id = lib_obj.register_patron(first_name, last_name, age, member_id)
        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertEqual(id, 1)

    def test_another_patron_exists_in_db(self):
        # Assume
        first_name = 'Sam'
        last_name = 'Wheeler'
        age = 27
        member_id = 100001

        fnamr = 'Winston'
        lname = 'Schmear'
        age_2 = 31
        member_id_2 = 100002

        # Action
        lib_obj = Library()
        lib_obj.db.get_patron_count()
        id = lib_obj.register_patron(first_name, last_name, age, member_id)
        id = lib_obj.register_patron(fnamr, lname, age_2, member_id_2)
        # Removes the instance of the db.json created
        if path.exists('db.json'):
            os.remove('db.json')

        # Assert
        self.assertEqual(id, 2)

    def test_patron_is_not_registered_in_db(self):
        # Assume
        first_name = 'Sam'
        last_name = 'Wheeler'
        age = 27
        member_id = 100001

        # Action
        lib_obj = Library()

        lib_obj.db.get_patron_count()
        id = lib_obj.register_patron(first_name, last_name, age, member_id)

        # Assert
        self.assertEqual(1, 2)

    def test_patron_has_borrowed_book(self):
        # Assume

        # Action

        # Assert
        pass

    def test_has_patron_borrowed_book_true(self):
        # Assume

        # Action

        # Assert
        pass

    def test_has_patron_borrowed_book_false(self):
        # Assume

        # Action

        # Assert
        pass

    def test_patron_has_returned_book(self):
        # Assume

        # Action

        # Assert
        pass

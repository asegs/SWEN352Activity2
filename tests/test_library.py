from unittest import TestCase
from unittest.mock import Mock

from library.library import Library

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
                'language': 'english'
            },
            {
                'language': 'hindi'
            },
            {
                'language': 'spanish'
            },
            {
                'language': 'russian'
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
        book_title = 'Something'
        # Action
        lib_obj = Library()
        lib_obj.api = Mock()
        lib_obj.api.get_book_info.return_value = book_language_list
        # Assert

        languages = lib_obj.get_languages_for_book(book_title)
        self.assertEqual(len(languages), len(book_language_list))
        pass

    def test_gets_one_language_for_the_book(self):
        # Assume

        # Action

        # Assert
        pass

    def test_gets_zero_language_for_no_book(self):
        # Assume

        # Action

        # Assert
        pass

    def test_gets_the_correct_languages_for_the_book(self):
        # Assume

        # Action

        # Assert
        pass

    def test_patron_added_to_library_db(self):
        # Assume

        # Action

        # Assert
        pass

    def test_patron_exists_in_library_db(self):
        # Assume

        # Action

        # Assert
        pass

    def test_patron_is_registered_in_db(self):
        # Assume

        # Action

        # Assert
        pass

    def test_patron_is_not_registered_in_db(self):
        # Assume

        # Action

        # Assert
        pass

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

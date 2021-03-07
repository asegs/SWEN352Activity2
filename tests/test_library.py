from unittest import TestCase
from unittest.mock import Mock


class TestLibrary(TestCase):
    import library.library as library

    def test_is_ebook(self):
        self.fail()

    def test_book_is_ebook(self):
        pass

    def test_book_is_not_ebook(self):
        pass

    def test_gets_book_count_for_more_than_zero(self):
        pass

    def test_gets_book_count_for_zero_books(self):
        pass

    def test_gets_book_count_if_no_book_is_there(self):
        pass

    def test_author_entered_for_book_is_true(self):
        pass

    def test_author_entered_for_book_is_false(self):
        pass

    def test_gets_languages_for_the_book(self):
        pass

    def test_gets_one_language_for_the_book(self):
        pass

    def test_gets_zero_language_for_no_book(self):
        pass

    def test_gets_the_correct_languages_for_the_book(self):
        pass

    def test_patron_added_to_library_db(self):
        pass

    def test_patron_exists_in_library_db(self):
        pass

    def test_patron_is_registered_in_db(self):
        pass

    def test_patron_is_not_registered_in_db(self):
        pass

    def test_patron_has_borrowed_book(self):
        pass

    def test_has_patron_borrowed_book_true(self):
        pass

    def test_has_patron_borrowed_book_false(self):
        pass

    def test_patron_has_returned_book(self):
        pass

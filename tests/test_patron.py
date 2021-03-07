import unittest

from src.library.patron import *


class TestPatron(unittest.TestCase):

    def test_create_patron_with_numbers(self):
        try:
            Patron(fname="12345", lname="last", age="15", memberID="1")
        except InvalidNameException as e:
            self.assertEqual(InvalidNameException, type(e))
        else:
            self.fail('InvalidNameException not raised')

    def test_add_borrowed_book(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        CuT.add_borrowed_book("Cat in the Hat")
        self.assertEqual('cat in the hat', CuT.get_borrowed_books()[0])

    def test_add_borrowed_book_twice(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        CuT.add_borrowed_book("Cat in the Hat")
        CuT.add_borrowed_book("Cat in the Hat")
        self.assertEqual(1, len(CuT.get_borrowed_books()))

    def test_return_borrowed_book(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        book = "Cat in the Hat"
        CuT.add_borrowed_book(book)
        CuT.return_borrowed_book(book)
        self.assertEqual(0, len(CuT.get_borrowed_books()))

    def test_return_not_borrowed_book(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        CuT.return_borrowed_book("not borrowed book")
        self.assertEqual(0, len(CuT.get_borrowed_books()))

    def test_eq_equal(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        other = Patron(fname="first", lname="last", age="15", memberID="1")
        result = CuT.__eq__(other)
        self.assertEqual(True, result)

    def test_eq_not_equal(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        other = Patron(fname="notsame", lname="notsame", age="15", memberID="1")
        result = CuT.__eq__(other)
        self.assertEqual(False, result)

    def test_ne_equal(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        other = Patron(fname="first", lname="last", age="15", memberID="1")
        result = CuT.__ne__(other)
        self.assertEqual(False, result)

    def test_ne_not_equal(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        other = Patron(fname="notsame", lname="notsame", age="15", memberID="1")
        result = CuT.__ne__(other)
        self.assertEqual(True, result)

    def test_get_fname(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        self.assertEqual("first", CuT.get_fname())

    def test_get_lname(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        self.assertEqual("last", CuT.get_lname())
    def test_get_age(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        self.assertEqual("15", CuT.get_age())
    def test_get_memberID(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        self.assertEqual("1", CuT.get_memberID())


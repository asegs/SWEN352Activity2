import unittest

from src.library.patron import *


class TestPatron(unittest.TestCase):

    def test_add_borrowed_book(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        CuT.add_borrowed_book("Cat in the Hat")
        self.assertEqual('cat in the hat', CuT.get_borrowed_books()[0])

    def test_add_borrowed_book_twice(self):
        CuT = Patron(fname="first", lname="last", age="15", memberID="1")
        CuT.add_borrowed_book("Cat in the Hat")
        CuT.add_borrowed_book("Cat in the Hat")
        self.assertEqual(1, len(CuT.get_borrowed_books()))

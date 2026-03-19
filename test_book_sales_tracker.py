"""Tests for the Book Sales Tracker system."""

import os
import tempfile
import pytest
from book_sales_tracker import Book, BookSalesTracker


@pytest.fixture
def temp_data_file():
    """Create a temporary file path for test data."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    os.remove(path)  # Remove the empty file so tracker starts fresh
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def tracker(temp_data_file):
    """Create a tracker instance with a temporary data file."""
    return BookSalesTracker(temp_data_file)


class TestBook:
    def test_book_creation(self):
        book = Book(title="Test Book", author="Test Author", isbn="123-456")
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.isbn == "123-456"
        assert book.total_sales == 0

    def test_book_with_initial_sales(self):
        book = Book(title="Test", author="Author", isbn="123", total_sales=100)
        assert book.total_sales == 100


class TestBookSalesTracker:
    def test_add_book(self, tracker):
        book = tracker.add_book("Test Book", "Author", "123-456", 100)
        assert book.title == "Test Book"
        assert book.total_sales == 100
        assert tracker.get_book("123-456") is not None

    def test_add_duplicate_book_raises_error(self, tracker):
        tracker.add_book("Book 1", "Author", "123")
        with pytest.raises(ValueError):
            tracker.add_book("Book 2", "Author", "123")

    def test_update_sales(self, tracker):
        tracker.add_book("Test", "Author", "123", 100)
        tracker.update_sales("123", 50)
        book = tracker.get_book("123")
        assert book.total_sales == 150

    def test_update_sales_nonexistent_book(self, tracker):
        with pytest.raises(KeyError):
            tracker.update_sales("nonexistent", 100)

    def test_bulk_update_sales(self, tracker):
        tracker.add_book("Book 1", "Author", "111", 100)
        tracker.add_book("Book 2", "Author", "222", 200)
        tracker.bulk_update_sales({"111": 50, "222": 100})
        assert tracker.get_book("111").total_sales == 150
        assert tracker.get_book("222").total_sales == 300

    def test_bulk_update_missing_isbn(self, tracker):
        tracker.add_book("Book 1", "Author", "111", 100)
        with pytest.raises(KeyError):
            tracker.bulk_update_sales({"111": 50, "999": 100})

    def test_get_top_sellers(self, tracker):
        tracker.add_book("Low", "Author", "1", 100)
        tracker.add_book("High", "Author", "2", 500)
        tracker.add_book("Mid", "Author", "3", 300)
        top = tracker.get_top_sellers(n=2)
        assert len(top) == 2
        assert top[0].title == "High"
        assert top[1].title == "Mid"

    def test_get_top_sellers_all(self, tracker):
        tracker.add_book("A", "Author", "1", 100)
        tracker.add_book("B", "Author", "2", 200)
        top = tracker.get_top_sellers()
        assert len(top) == 2

    def test_get_total_sales(self, tracker):
        tracker.add_book("A", "Author", "1", 100)
        tracker.add_book("B", "Author", "2", 200)
        assert tracker.get_total_sales() == 300

    def test_persistence(self, temp_data_file):
        tracker1 = BookSalesTracker(temp_data_file)
        tracker1.add_book("Persisted Book", "Author", "123", 500)

        tracker2 = BookSalesTracker(temp_data_file)
        book = tracker2.get_book("123")
        assert book is not None
        assert book.title == "Persisted Book"
        assert book.total_sales == 500

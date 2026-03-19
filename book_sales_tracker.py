"""
Book Sales Tracker - A system to track total book sales and display top sellers.
"""

__version__ = "0.1.0"

import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Book:
    """Represents a book with its sales information."""
    title: str
    author: str
    isbn: str
    total_sales: int = 0


class BookSalesTracker:
    """
    Tracks book sales and provides top-selling books list.

    Data is persisted to a JSON file and automatically loaded on initialization.
    """

    def __init__(self, data_file: str = "sales_data.json"):
        """
        Initialize the tracker with a data file path.

        Args:
            data_file: Path to the JSON file for storing sales data.
        """
        self.data_file = Path(data_file)
        self.books: dict[str, Book] = {}  # ISBN -> Book mapping
        self._load_data()

    def _load_data(self) -> None:
        """Load existing sales data from the JSON file."""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for book_data in data.get('books', []):
                    book = Book(**book_data)
                    self.books[book.isbn] = book

    def _save_data(self) -> None:
        """Save current sales data to the JSON file."""
        data = {
            'last_updated': datetime.now().isoformat(),
            'books': [asdict(book) for book in self.books.values()]
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_book(self, title: str, author: str, isbn: str, initial_sales: int = 0) -> Book:
        """
        Add a new book to track.

        Args:
            title: Book title.
            author: Book author.
            isbn: Unique ISBN identifier.
            initial_sales: Starting sales count.

        Returns:
            The created Book object.

        Raises:
            ValueError: If a book with the same ISBN already exists.
        """
        if isbn in self.books:
            raise ValueError(f"Book with ISBN {isbn} already exists")

        book = Book(title=title, author=author, isbn=isbn, total_sales=initial_sales)
        self.books[isbn] = book
        self._save_data()
        return book

    def update_sales(self, isbn: str, sales_count: int) -> list[Book]:
        """
        Update sales for a book and return the current top sellers.

        Args:
            isbn: ISBN of the book to update.
            sales_count: Number of sales to add.

        Returns:
            List of top-selling books after the update.

        Raises:
            KeyError: If no book with the given ISBN exists.
        """
        if isbn not in self.books:
            raise KeyError(f"No book found with ISBN {isbn}")

        self.books[isbn].total_sales += sales_count
        self._save_data()

        top_sellers = self.get_top_sellers()
        self._print_top_sellers(top_sellers)
        return top_sellers

    def bulk_update_sales(self, updates: dict[str, int]) -> list[Book]:
        """
        Update sales for multiple books at once.

        Args:
            updates: Dictionary mapping ISBN to sales count to add.

        Returns:
            List of top-selling books after all updates.

        Raises:
            KeyError: If any ISBN is not found.
        """
        missing = [isbn for isbn in updates if isbn not in self.books]
        if missing:
            raise KeyError(f"No books found with ISBNs: {missing}")

        for isbn, sales_count in updates.items():
            self.books[isbn].total_sales += sales_count

        self._save_data()

        top_sellers = self.get_top_sellers()
        self._print_top_sellers(top_sellers)
        return top_sellers

    def get_top_sellers(self, n: Optional[int] = None) -> list[Book]:
        """
        Get the top-selling books.

        Args:
            n: Number of top sellers to return. If None, returns all books sorted by sales.

        Returns:
            List of books sorted by total sales (descending).
        """
        sorted_books = sorted(
            self.books.values(),
            key=lambda b: b.total_sales,
            reverse=True
        )
        if n is not None:
            return sorted_books[:n]
        return sorted_books

    def get_total_sales(self) -> int:
        """Get the total sales across all books."""
        return sum(book.total_sales for book in self.books.values())

    def get_book(self, isbn: str) -> Optional[Book]:
        """Get a book by its ISBN."""
        return self.books.get(isbn)

    def _print_top_sellers(self, books: list[Book], n: int = 10) -> None:
        """Print the top sellers in a formatted way."""
        display_books = books[:n]
        print(f"\n{'='*60}")
        print(f"TOP {len(display_books)} BEST-SELLING BOOKS")
        print(f"{'='*60}")
        for i, book in enumerate(display_books, 1):
            print(f"{i:2}. {book.title}")
            print(f"    Author: {book.author}")
            print(f"    ISBN: {book.isbn}")
            print(f"    Total Sales: {book.total_sales:,}")
            print()
        print(f"Total sales across all books: {self.get_total_sales():,}")
        print(f"{'='*60}\n")

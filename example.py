"""
Example usage of the Book Sales Tracker system.
"""

from book_sales_tracker import BookSalesTracker


def main():
    # Initialize the tracker (will create/load sales_data.json)
    tracker = BookSalesTracker("sales_data.json")

    # Add some books
    print("Adding books to the system...")
    try:
        tracker.add_book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", 15000)
        tracker.add_book("1984", "George Orwell", "978-0451524935", 25000)
        tracker.add_book("To Kill a Mockingbird", "Harper Lee", "978-0061120084", 20000)
        tracker.add_book("Pride and Prejudice", "Jane Austen", "978-0141439518", 18000)
        tracker.add_book("The Catcher in the Rye", "J.D. Salinger", "978-0316769488", 12000)
        tracker.add_book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "978-0590353427", 50000)
        tracker.add_book("The Hobbit", "J.R.R. Tolkien", "978-0547928227", 30000)
        tracker.add_book("Brave New World", "Aldous Huxley", "978-0060850524", 10000)
        print("Books added successfully!\n")
    except ValueError as e:
        print(f"Some books already exist: {e}\n")

    # Update sales for a single book (this will automatically print top sellers)
    print("Updating sales for '1984' (+5000 copies)...")
    tracker.update_sales("978-0451524935", 5000)

    # Bulk update sales for multiple books
    print("Bulk updating sales for multiple books...")
    tracker.bulk_update_sales({
        "978-0590353427": 10000,  # Harry Potter
        "978-0547928227": 8000,   # The Hobbit
        "978-0743273565": 3000,   # The Great Gatsby
    })

    # Get top 5 sellers specifically
    print("\nTop 5 best-selling books:")
    top_5 = tracker.get_top_sellers(n=5)
    for i, book in enumerate(top_5, 1):
        print(f"  {i}. {book.title} - {book.total_sales:,} copies")

    # Get total sales
    print(f"\nTotal sales across all books: {tracker.get_total_sales():,}")


if __name__ == "__main__":
    main()

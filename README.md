# Book Sales Tracker

A Python system to track book sales and display top-selling books.

## Installation

```bash
pip install book-sales-tracker
```

Or install from a release:
```bash
pip install https://github.com/jeffzhu503/book-sales-tracker/releases/download/v0.1.0/book_sales_tracker-0.1.0-py3-none-any.whl
```

## Usage

```python
from book_sales_tracker import BookSalesTracker

# Initialize tracker (data persists to JSON file)
tracker = BookSalesTracker("sales_data.json")

# Add books
tracker.add_book("1984", "George Orwell", "978-0451524935", 25000)
tracker.add_book("The Hobbit", "J.R.R. Tolkien", "978-0547928227", 30000)

# Update sales (automatically displays top sellers)
tracker.update_sales("978-0451524935", 5000)

# Bulk update
tracker.bulk_update_sales({
    "978-0451524935": 1000,
    "978-0547928227": 2000,
})

# Get top N sellers
top_5 = tracker.get_top_sellers(n=5)

# Get total sales
total = tracker.get_total_sales()
```

## License

MIT

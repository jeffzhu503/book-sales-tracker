# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python system for tracking book sales and displaying top-selling books. Data is persisted to JSON files.

## Running the Project

```bash
# Run the example script
python example.py

# Or import and use directly
python -c "from book_sales_tracker import BookSalesTracker; t = BookSalesTracker(); print(t.get_top_sellers(5))"
```

## Architecture

- **`book_sales_tracker.py`**: Core module containing:
  - `Book` dataclass: Represents a book (title, author, isbn, total_sales)
  - `BookSalesTracker` class: Main tracker with JSON persistence

- **`example.py`**: Demonstrates usage patterns

## Key Design Decisions

- Books are keyed by ISBN (unique identifier)
- `update_sales()` and `bulk_update_sales()` automatically print top sellers after each update
- Data auto-saves to JSON after every modification
- `get_top_sellers(n)` returns all books sorted by sales when `n` is None

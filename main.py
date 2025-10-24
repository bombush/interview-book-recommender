import pandas as pd
import loader as ld

def get_user_yes_no_input(prompt: str) -> bool:
    """Get validated yes/no input from user."""
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Invalid input. Please enter Y or N.")

def search_books_by_title(books: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """Search for books by title (case-insensitive)."""
    contains_mask = books['Book-Title'].str.contains(
        search_term, case=False, na=False, regex=False
    )
    return books[contains_mask]

def search_books_by_isbn(books: pd.DataFrame, isbn: str) -> pd.DataFrame:
    """Search for books by ISBN."""
    return books[books['ISBN'] == isbn]

def display_books(books: pd.DataFrame, columns: list[str] = None):
    """Display books in a readable format."""
    if columns is None:
        columns = ['ISBN', 'Book-Title', 'Book-Author']
    
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.max_rows", None)
    print(books[columns])
    pd.reset_option("display.max_colwidth")
    pd.reset_option("display.max_rows")

def is_isbn(input_str: str) -> bool:
    """Check if the input string is a valid ISBN (10 or 13 digits)."""
    cleaned = input_str.replace('-', '').replace(' ', '')
    return cleaned.isdigit() and len(cleaned) in [10, 13]

def handle_book_search(books: pd.DataFrame) -> tuple[bool, pd.DataFrame]:
    """
    Handle a single book search interaction.
    Returns: (success, matching_books)
    """
    user_book = input("Enter title or ISBN of your favorite book: ").strip()
    if is_isbn(user_book):
        matching_books = search_books_by_isbn(books, user_book)
    else:
        matching_books = search_books_by_title(books, user_book)
    
    count = len(matching_books)
    
    if count == 0:
        print("No books found with that title. Please try again.")
        return False, pd.DataFrame()
    
    if count > 1:
        print(f"\n{count} books found with that title. Please be more specific:\n")
        display_books(matching_books)
        return False, pd.DataFrame()
    
    # Exactly one book found
    book = matching_books.iloc[0]
    display_books(matching_books)
    return True, matching_books

def get_similar_books(book_isbn: str) -> list[str]:
    """Get list of books similar to the given book."""
    # @TODO: implement recommendation algorithm
    return []

def main():
    """Main application loop."""
    books = ld.load_books()
    
    first_run = True
    while True:
        if not first_run:
            if not get_user_yes_no_input("\nDo you want to try another book? [Y/N]: "):
                print("Thank you for using the book recommender!")
                break
        first_run = False
        
        success, found_books = handle_book_search(books)
        
        if not success:
            continue
        
        # Get and display similar books
        book_index = found_books.index[0]
        similar_books = get_similar_books(book_index)

        if similar_books:
            print(f"\nBooks similar to '{found_books.iloc[0]['Book-Title']}':")
            for book in sorted(similar_books):
                print(f"  - {book}")
        else:
            print("\nNo similar books found.")

if __name__ == "__main__":
    main()
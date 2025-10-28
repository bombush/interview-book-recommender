import pandas as pd
import loader as ld
from typing import Optional

import recommender as rec

def get_user_yes_no_input(prompt: str) -> bool:
    """Get validated yes/no input from user."""
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Invalid input. Please enter Y or N.")

def display_books(books: pd.DataFrame, columns: Optional[list[str]]):
    """Display books in a readable format."""
    if columns is None:
        columns = ['ISBN', 'Book-Title', 'Book-Author']
    
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.max_rows", None)
    print(books[columns])
    pd.reset_option("display.max_colwidth")
    pd.reset_option("display.max_rows")

def search_books_by_title(books: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """Search for books by title (case-insensitive)."""
    contains_mask = books['Book-Title'].str.contains(
        search_term, case=False, na=False, regex=False
    )
    return books[contains_mask]

def search_books_by_isbn(books: pd.DataFrame, isbn: str) -> pd.DataFrame:
    """Search for books by ISBN."""
    return books[books['ISBN'] == isbn]

def is_isbn(input_str: str) -> bool:
    """Check if the input string is a valid ISBN (10 or 13 digits)."""
    cleaned = input_str.replace('-', '').replace(' ', '')

    # if last character is X, drop it and check if the rest rest of the 9 characters are digits
    # (X is used instead of 10 in ISBN-10 checksum. See https://www.isbn.org/faqs_general_questions#:~:text=Why%20do%20some%20ISBNs%20end,assign%20ISBNs%20to%20a%20publisher?)
    if(len(cleaned) == 10):
        if cleaned[-1].upper() == 'X':
            return cleaned[:-1].isdigit()
        else:
            return cleaned.isdigit()
    elif(len(cleaned) == 13):
        return cleaned.isdigit()
    else:
        return False


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
        display_books(matching_books, None)
        return False, pd.DataFrame()
    
    # Exactly one book found
    display_books(matching_books, None)
    return True, matching_books

def get_similar_books(book: pd.Series) -> pd.DataFrame:
    """Get list of books similar to the given book."""
    print(type(book))
    print(book)
    book_isbn = book['ISBN']
    similar_books = rec.find_correlated_books_by_isbn(book_isbn).sort_values('corr', ascending=False).head(10)
    return similar_books

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
        book_index = found_books.iloc[0]
        similar_books = get_similar_books(book_index)

        if not similar_books.empty:
            print(f"\nBooks similar to '{found_books.iloc[0]['Book-Title']}':")
            print(similar_books)
        else:
            print("\nNo similar books found.")


if __name__ == "__main__":
    main()
##
# Recommender module
# 
# Conversion of old/book_rec_standalone.py into a general-user function.
#

from typing import Any
import pandas as pd
import numpy as np
import loader as ld

def prepare_dataset() -> pd.DataFrame:
      # Load data
    ratings = ld.load_ratings()
    ratings = ratings[ratings['Book-Rating'] != 0]
    books = ld.load_books()
    
    # Merge ratings with book information
    # @TODO: ISBN is not guaranteed to be unique (but we assume it is here)
    dataset = pd.merge(ratings, books, on=['ISBN'])
    dataset['Book-Title'] = dataset['Book-Title'].str.lower()
    dataset['Book-Author'] = dataset['Book-Author'].str.lower()
    dataset['ISBN'] = dataset['ISBN'].str.lower()
    return dataset


def find_by_isbn(dataset_lowercase: pd.DataFrame, book_isbn: str, min_ratings_threshold: int = 8) -> pd.DataFrame:
     # Find the book by ISBN
    target_book = dataset_lowercase[dataset_lowercase['ISBN'] == book_isbn.lower()]
    
    if target_book.empty:
        print(f"Book with ISBN {book_isbn} not found in dataset.")
        return pd.DataFrame(columns=['book', 'corr', 'avg_rating'])
    
    # Get the book title (use first match if multiple editions, but ISBN should be unique)
    # @TODO: iloc is deprecated, fix
    target_book_title = target_book.iloc[0]['Book-Title']
    print(f"Finding recommendations for book: '{target_book_title}' by {target_book['Book-Author'].values[0]}")

    # Find all users who rated this book
    book_readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title'] == target_book_title) & (dataset_lowercase['Book-Author'] == target_book['Book-Author'].values[0])]
    book_readers.drop_duplicates(inplace=True)

    book_readers = np.unique(book_readers)

    if len(book_readers) == 0:
        print(f"No ratings found for book with ISBN {book_isbn}.")
        return pd.DataFrame(columns=['book', 'corr', 'avg_rating'])
    
    # Get all books rated by these users
    books_of_readers = dataset_lowercase[dataset_lowercase['User-ID'].isin(book_readers)]
    
    # Count ratings per book
    number_of_rating_per_book = books_of_readers.groupby(['Book-Title']).agg('count').reset_index()
    
    # Select only books with sufficient ratings
    books_to_compare = number_of_rating_per_book['Book-Title'][
        number_of_rating_per_book['User-ID'] >= min_ratings_threshold
    ]
    list_books_to_compare = books_to_compare.tolist()
    del books_to_compare

    if len(list_books_to_compare) <= 1:  # Only the target book or no books
        print(f"Insufficient data to generate recommendations (only {len(list_books_to_compare)} books with {min_ratings_threshold}+ ratings).")
        return pd.DataFrame(columns=['book', 'corr', 'avg_rating'])
    
    # Filter ratings data
    ratings_data_raw = books_of_readers[['User-ID', 'Book-Rating', 'Book-Title']][
        books_of_readers['Book-Title'].isin(list_books_to_compare)
    ]
    
    print(ratings_data_raw.head())
    # Group by User and Book and compute mean (handles multiple ratings by same user)
    ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean().to_frame().reset_index()
    
    # Pivot to create user-book rating matrix
    dataset_for_corr = ratings_data_raw_nodup.pivot(
        index='User-ID', 
        columns='Book-Title', 
        values='Book-Rating'
    )
    
    # Check if target book is in the correlation dataset
    if target_book_title not in dataset_for_corr.columns:
        print(f"Target book '{target_book_title}' not found in correlation dataset.")
        return pd.DataFrame(columns=['book', 'corr', 'avg_rating'])
    
    target_book = dataset_for_corr[target_book_title]
    dataset_for_corr.drop([target_book_title], axis=1, inplace=True)    
   

    # Compute correlations
    correlations_df = dataset_for_corr.corrwith(target_book, axis=0)

    titles = correlations_df.index.tolist()
    ratings = ratings_data_raw_nodup.groupby('Book-Title')['Book-Rating'].mean().fillna(0)

    final_df = pd.DataFrame(data={'book': titles, 'corr': correlations_df.values})

    final_df =final_df.merge(right=ratings, left_on='book', how='left', right_on='Book-Title')
    final_df.rename(columns={'Book-Rating': 'avg_rating'}, inplace=True)
    final_df= final_df.dropna(subset=['corr'])

    #print(final_df.head())

    return final_df

# refactored function to satisfy the API for the CLI app
def find_correlated_books_by_isbn(book_isbn: str, min_ratings_threshold: int = 8) -> pd.DataFrame:
    """
    Recommend books similar to the given book based on user rating correlations.
    
    This function finds users who rated the specified book, then computes correlation
    between that book's ratings and ratings of other books by the same users.
    
    Args:
        book_isbn: ISBN of the book to find recommendations for
        min_ratings_threshold: Minimum number of ratings required for a book to be considered (default: 8)
        top_n: Number of top recommendations to return (default: 10)
    
    Returns:
        DataFrame with columns ['book', 'corr', 'avg_rating'] sorted by correlation (descending)
        Returns empty DataFrame if book not found or insufficient data
    """
    dataset_lowercase = prepare_dataset()
    return find_by_isbn(dataset_lowercase, book_isbn, min_ratings_threshold)
    
   
##
# Recommender module
# 
# Conversion of old/book_rec_standalone.py into a general-user function.
#

import pandas as pd
import numpy as np
import loader as ld

def prepare_dataset() -> pd.DataFrame:
      # Load data
    ratings = ld.load_ratings()
    ratings = ratings[ratings['Book-Rating'] != 0]
    books = ld.load_books()
    
    # Merge ratings with book information
    dataset = pd.merge(ratings, books, on=['ISBN'])
    dataset_lowercase = dataset.apply(lambda x: x.str.lower() if x.dtype == 'object' else x)
    return dataset_lowercase

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
    
    # Find the book by ISBN
    target_book = dataset_lowercase[dataset_lowercase['ISBN'] == book_isbn.lower()]
    
    if target_book.empty:
        print(f"Book with ISBN {book_isbn} not found in dataset.")
        return pd.DataFrame(columns=['book', 'corr', 'avg_rating'])
    
    # Get the book title (use first match if multiple editions, but ISBN should be unique)
    target_book_title = target_book.iloc[0]['Book-Title']

    # @TODO: try to find book by BookTitle and Author if ISBN not found

    # Find all users who rated this book
    book_readers = dataset_lowercase['User-ID'][dataset_lowercase['ISBN'] == book_isbn.lower()]
    book_readers = book_readers.tolist()
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
    books_to_compare = books_to_compare.tolist()
    
    if len(books_to_compare) <= 1:  # Only the target book or no books
        print(f"Insufficient data to generate recommendations (only {len(books_to_compare)} books with {min_ratings_threshold}+ ratings).")
        return pd.DataFrame(columns=['book', 'corr', 'avg_rating'])
    
    # Filter ratings data
    ratings_data_raw = books_of_readers[['User-ID', 'Book-Rating', 'Book-Title']][
        books_of_readers['Book-Title'].isin(books_to_compare)
    ]
    
    # Group by User and Book and compute mean (handles multiple ratings by same user)
    ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()
    ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()
    
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
    
    # Create dataset without the target book
    dataset_of_other_books = dataset_for_corr.copy(deep=False)
    dataset_of_other_books.drop([target_book_title], axis=1, inplace=True)
    
    # Compute correlations
    book_titles = []
    correlations = []
    avgrating = []
    
    for book_title in list(dataset_of_other_books.columns.values):
        book_titles.append(book_title)
        corr_value = dataset_for_corr[target_book_title].corr(dataset_of_other_books[book_title])
        correlations.append(corr_value)
        
        mean = (ratings_data_raw[ratings_data_raw['Book-Title'] == book_title]
                .groupby('Book-Title')['Book-Rating'].mean())
        avgrating.append(mean[book_title] if book_title in mean.index else 0)
    
    # Create final dataframe
    corr_df = pd.DataFrame(
        list(zip(book_titles, correlations, avgrating)), 
        columns=['book', 'corr', 'avg_rating']
    )
    
    # Remove rows with NaN correlations and sort
    corr_df = corr_df.dropna(subset=['corr'])
    
    return corr_df
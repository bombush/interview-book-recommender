import pandas as pd

from typing import Optional

_ratings : Optional[pd.DataFrame] = None
_books: Optional[pd.DataFrame] = None

def load_ratings() -> pd.DataFrame:
    global _ratings
    if(_ratings == None):
        _ratings = pd.read_csv('Downloads/Ratings.csv', encoding='utf8', sep=',')
    
    return _ratings

# returns Pandas DataFrame
def load_books() -> pd.DataFrame:
    global _books
    if(_books == None):
        _books = pd.read_csv('Downloads/Books.csv',  encoding='utf8', sep=',',on_bad_lines='warn', dtype={'Book-Title': str, 'Book-Author': str, 'Year-Of-Publication': str, 'Publisher': str})
    return _books


# import
import pandas as pd
import numpy as np

##
# NOTE: are correlations with low rating useful? Might be: for people who hated LotR can be recommended books liked by other people who hated LotR. 
#       That is quite a broad scope. Can the results be any useful? Maybe for readers of fantasy: 
#       people who like fantasy but hate Tolkien might like Pratchett or Sapkowski, but people who hate Tolkien because they hate fantasy in general, 
#       probably form a very diverse group (readers of high literature, crime fiction, romance, etc.).
#
# General idea:
# - We are compiting data for recommendation of books similar to The Fellowship of the Ring
# - similarity factors:
#  - 
# #

# load ratings
# NOTE: why is not everything utf8? It's the 21st century...
# @TODO: check that the files are actually encoded in cp1251.
ratings = pd.read_csv('Downloads/BX-Book-Ratings.csv', encoding='cp1251', sep=';')
ratings = ratings[ratings['Book-Rating']!=0]

# load books
books = pd.read_csv('Downloads/BX-Books.csv',  encoding='cp1251', sep=';',on_bad_lines='warn')

#users_ratigs = pd.merge(ratings, users, on=['User-ID'])
dataset = pd.merge(ratings, books, on=['ISBN'])
# @TODO: normalized case. Should we normalize accents as well?
dataset_lowercase=dataset.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)

# @TODO: 'tolkien' is a poor criterion. Might match other authors with 'tolkien' in their name.
# @TODO: match with j.r.r. tolkien, convert to numeric id, then match with that id?
# NOTE: I see, tolkien_readers are actually not readers of Tolkien, but readers of the Fellowship of the Ring, written by Tolkien. confusing var name :)
# @TODO: we should be working with book ids already here (not strictly needed for CLI app, but good for migration to web-based frontend later)
tolkien_readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title']=='the fellowship of the ring (the lord of the rings, part 1)') & (dataset_lowercase['Book-Author'].str.contains("tolkien"))]
tolkien_readers = tolkien_readers.tolist()
tolkien_readers = np.unique(tolkien_readers)

# final dataset
books_of_tolkien_readers = dataset_lowercase[(dataset_lowercase['User-ID'].isin(tolkien_readers))]

# Number of ratings per other books in dataset
number_of_rating_per_book = books_of_tolkien_readers.groupby(['Book-Title']).agg('count').reset_index()

#select only books which have actually higher number of ratings than threshold
books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= 8]
books_to_compare = books_to_compare.tolist()

ratings_data_raw = books_of_tolkien_readers[['User-ID', 'Book-Rating', 'Book-Title']][books_of_tolkien_readers['Book-Title'].isin(books_to_compare)]

# group by User and Book and compute mean
# NOTE: does this mean that a user can rate the same book multiple times? If that is our assumption about the data, why not take the latest rating or precompute?
ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()

# reset index to see User-ID in every row
# @TODO: why reset index?
ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()

# @TODO: why pivot here? Is that any faster for later processing than just using groupby?
dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')

# why is this a list? 
# @TODO: duplicate literal string: book title. Should be a constant or variable.
LoR_list = ['the fellowship of the ring (the lord of the rings, part 1)']

result_list = []
worst_list = []

# for each of the trilogy book compute:
# NOTE: I see. The intention was to process the whole trilogy, but there is only one book in the list. Also, we are only using one book anyway.
# @TODO: remove the confusing forloop
for LoR_book in LoR_list:
    
    #Take out the Lord of the Rings selected book from correlation dataframe
    ## @TODO: optimize: drop 
    ## @TODO: why copy on each iteration? Can't we just skip the book (branch predictor cache miss possible, but avoids memory reallocation). Look into the docs of pandas how copy is implemented. Is it COW?
    dataset_of_other_books = dataset_for_corr.copy(deep=False)
    dataset_of_other_books.drop([LoR_book], axis=1, inplace=True)
      
    # empty lists
    book_titles = []
    correlations = []
    avgrating = []

    # corr computation
    for book_title in list(dataset_of_other_books.columns.values):
        book_titles.append(book_title)
        # NOTE: find similarity?
        correlations.append(dataset_for_corr[LoR_book].corr(dataset_of_other_books[book_title]))
        tab=(ratings_data_raw[ratings_data_raw['Book-Title']==book_title].groupby(ratings_data_raw['Book-Title']).mean())
        avgrating.append(tab['Book-Rating'].min())
    # final dataframe of all correlation of each book   
    corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avgrating)), columns=['book','corr','avg_rating'])
    corr_fellowship.head()

    # top 10 books with highest corr
    result_list.append(corr_fellowship.sort_values('corr', ascending = False).head(10))
    
    #worst 10 books
    worst_list.append(corr_fellowship.sort_values('corr', ascending = False).tail(10))
    
print("Correlation for book:", LoR_list[0])
#print("Average rating of LOR:", ratings_data_raw[ratings_data_raw['Book-Title']=='the fellowship of the ring (the lord of the rings, part 1'].groupby(ratings_data_raw['Book-Title']).mean()))
rslt = result_list[0]
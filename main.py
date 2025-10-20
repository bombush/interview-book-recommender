import pandas as pd

# @TODO: bring it all together
import loader as ld

# this is actually not that great way to do it, but ok for CLI app
def user_wants_to_look_for_books():
    yield True # no menu on first run

    while True:
        should_retry = input("Do you want to try another book? [Y/N]")
        if(should_retry.lower() not in ['y', 'n']):
            print("Invalid input. Please enter Y or N.")
            yield from user_wants_to_look_for_books()
        yield should_retry.lower() == 'y'




books = ld.load_books()
main_loop = user_wants_to_look_for_books()
while next(main_loop):
    user_book = input("Enter title of you favorite book: ")
    contains_mask = books['Book-Title'].str.contains(user_book, case=False, na=False, regex=False)
    books_user_interested = books[contains_mask]
    
    count_user_books = len(books_user_interested)
    if(count_user_books == 0):
        print("No books found with that title. Please try again.")
        continue

    if(count_user_books > 1):
        print("Multiple books found with that title. Please be more specific:\n")

        pd.set_option("display.max_colwidth", None)
        pd.set_option("display.max_rows", None)
        print(books_user_interested[['Book-Title', 'Book-Author']])
        pd.reset_option("display.max_colwidth")
        pd.reset_option("display.max_rows")

        continue

    # exactly one book found
    print("Found book:", books_user_interested.iloc[0]['Book-Title'], "by", books_user_interested.iloc[0]['Book-Author'])

    exit(0)




    # user_book to lowercase
    user_book_lower = user_book.lower()
    print("You entered:", user_book_lower)

    # get similar books
    similar_books = []  # @TODO: call the function that gets similar books
    similar_books.sort()

    print("Similar books", user_book, ":")


    for book in similar_books:
        print(book)

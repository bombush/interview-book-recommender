import streamlit as st
from streamlit import session_state as ss

import pandas as pd

import loader as ld
import recommender as rec

st.set_page_config(page_title="Book Recommender", page_icon="📚", layout="wide")


@st.cache_data(show_spinner=True)
def get_books() -> pd.DataFrame:
    return ld.load_books()


def search_books(books: pd.DataFrame, query: str) -> tuple[pd.DataFrame, bool]:
    """Search by ISBN (exact, case-insensitive) first; if not found, search title contains.
    Returns (matches, searched_by_isbn).
    """
    q = (query or "").strip()
    if not q:
        return books.iloc[0:0], False

    # Try ISBN exact match (case-insensitive, trimmed)
    isbn_matches = books[
        books["ISBN"].astype(str).str.strip().str.casefold() == q.casefold()
    ]
    if not isbn_matches.empty:
        return isbn_matches, True

    # Fall back to title contains (case-insensitive)
    title_matches = books[books["Book-Title"].astype(str).str.contains(q, case=False, na=False)]
    return title_matches, False


def main():
    st.title("📚 Book Recommender")

    with st.sidebar:
        st.header("Settings")
        min_ratings_threshold = st.slider("Min ratings per similar book", 1, 50, 8, 1)
        top_n = st.slider("Top N recommendations", 5, 50, 10, 1)

    st.write("Enter a book title or ISBN. If multiple matches are found, select one to see recommendations.")
    query = st.text_input("Book title or ISBN", placeholder="e.g., The Fellowship of the Ring or 0345339703")

    books = get_books()

    matches: pd.DataFrame | None = None

    if st.button("Search", type="primary"):
        matches, by_isbn = search_books(books, query)
        ss['matches'] = matches

    if 'matches' in ss and ss['matches'].empty:
        st.warning("No books found. Try a different query.")
    elif 'matches' in ss and ss['matches'] is not None:
        options = [
            f"{row['Book-Title']} — {row['Book-Author']} ({row['ISBN']})" for _, row in ss['matches'].iterrows()
        ]
        choice = st.selectbox("Select a book", options, key="book_selectbox")
        if choice:
            selected_isbn = choice.split("(")[-1].rstrip(")").strip()

    # If we have a selected ISBN, run recommender
    if ss['book_selectbox'] is not "":
        selected_isbn = ss['book_selectbox'].split("(")[-1].rstrip(")").strip()
        with st.spinner("Finding similar books..."):
            recs = rec.find_correlated_books_by_isbn(selected_isbn, min_ratings_threshold=min_ratings_threshold)

        if recs is None or recs.empty:
            st.warning("No similar books found.")
            return

        # Show recommendations table (book title and score); limit to top_n
        show_cols = [c for c in ["book", "corr", "avg_rating"] if c in recs.columns]
        st.subheader("Recommendations")
        st.dataframe(recs[show_cols].sort_values(show_cols[1] if len(show_cols) > 1 else show_cols[0], ascending=False).head(top_n), use_container_width=True)


if __name__ == "__main__":
    main()
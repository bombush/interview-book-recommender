### 2025-10-16
- setting up the venv
- looking for basic syntax errors
- learning about how indexers work in Pandas. Looking into under-the-hood implementation of Pandas ``DataFrames``.
    - ``NumPy`` or ``Apache Arrow``
    - ``NumPy`` is backed by C array of integers, but uses objects for strings (jumps in memory)
    - ``Apache Arrow`` - multiplatform, common language between different data frameworks. Strings backed by a contiguous array of characters. Faster CMP: can use SIMD instructions (SSE, AVX). Might be useful for comparing book titles. Not so easy for non-English though because of accents of differences in spelling (see Czech accents, Japanese Kanji/Hiragana usage and non-standard orthography). If I want to use SIMD instructions for strcmp for non-English I need to normalize the ANSI+ strings first. Is Apache Arrow locale-aware? (this is premature optimization ofc, but juicily low-level :D)
- funny error: Pandas coerces the book title 1984 into a numeric value and crashes. Why?
- frustration: I want static typing in Python > the code would be so much more readable. Also, dynamic typing is hardly useful when I need to optimize for speed on large datasets :) (grumble grumble from a C++ veteran)
- I need to familiarize myself with different correllations: ‘pearson’, ‘kendall’, ‘spearman’ [@STUDY] . Probably something to do with distances in an euclidean space. Everything is distances (or angles) in Euclidean space :)
- I'm drowning in theory. Let's get back to the script and move along a little bit from the engineering perspective
- @STUDY pivot tables
- Thoughts on lookups of book names: should we work with int32 bookID instead of book name? I think so, even with SIMD strcmp, lookup of integers should be faster. Also, for large datasets, length of strings may play a role: more integers fit in L1 cache (up to 80KB per core on Intel Xeon) so int lookup should scale better.
Cool, there's also pandas acceleration available on Nvidia GPUs! (https://developer.nvidia.com/blog/pandas-dataframe-tutorial-beginners-guide-to-gpu-accelerated-dataframes-in-python/)
- Note on the usefulness of correlation:  are correlations with low rating useful? Might be: for people who hated LotR can be recommended books liked by other people who hated LotR. That is quite a broad scope. Can the results be any useful? Maybe for readers of fantasy: 
people who like fantasy but hate Tolkien might like Pratchett or Sapkowski, but people who hate Tolkien because they hate fantasy in general, 
probably form a very diverse group (readers of high literature, crime fiction, romance, etc.).
- Note on duplicates: Multiple editions of the same books can be released with different ISBN. Title of the book can have subtle differences between editions but are conceptually the same book. Can we take that into account smh without resorting to manually annotating possible duplicates?
- How are pivot tables implemented under the hood?

- @TODO afternoon: look into functions tolist() vs. to_list() etc.
- @TODO afternoon: simple code: downloading datasets, frontend maybe etc. 
- @TODO afternoon: read about recommendation engines on Medium: [insert link here]


### 2025-10-17
Oh I found out you can overload operators in Python. That makes the script lot less confusing.
@TODO:  study groupby and other iterator objects
@TODO: i have this: 
```python
print(ratings_data_raw[ratings_data_raw['Book-Title']==book_title].groupby(ratings_data_raw['Book-Title'])['Book-Rating'].mean()) 
```
@TODO:How do I add new column?
I see... df == df returns a boolean mask usable for further filtering

Series is implemented as contiguous array of values and index. Index can be hashtable (Index. Lookup in O(1)), positional lookup for sequential indices (RangeIndex O(1)) or fallback to sequential scan. Custom implementation of the lookup engine is possible as well 
```python
    Index._engine is a C-backed engine (libpandas) for fast lookup.

It can be:

Int64Engine for integers (direct positional lookup)

Float64Engine for floats

ObjectEngine for strings / objects (hash table)

Lookup steps:

_engine.get_loc(label) → returns integer position.

Use that integer to fetch values[position].
``` 

TO STUDY: Each Series holds its data in a NumPy array (or an ExtensionArray for special dtypes like Categorical,

Now I need to figure out why correlation requires wide-form data (in other words, why pivot() is used in the script)

### 2024-10-20

I can parallelize processing using Dask

Careful about chained indexing
```
4. Chained indexing warning
df[df["A"] > 1]["B"] = 10  # ⚠ SettingWithCopyWarning


Here, df[df["A"] > 1] creates a new DataFrame.

Modifying "B" might not affect the original df.

Best practice:

df.loc[df["A"] > 1, "B"] = 10


.loc modifies the original safely.
```

### 2024-10-24
TODO: for better data quality, let the users group together different editions of the same book (or maybe make it automatic?)

Data quality fixes:
- lowercase
- unique (use ISBN for uniqueness)
- group multiple book editions together under a "work-ID". This will need some heuristics as well as manual classification for some books

### 2024-10-25
Note: ISBN is not guaranteed to be unique!

Copilot optimization Suggestions:
```
Removed the whole-DataFrame lowercasing pass and only normalized the text columns we actually need.
Replaced the per-column correlation loop with a vectorized correlation using Pandas’ corrwith.
Avoided counting all columns when computing popularity; used groupby.size() to compute the rating count faster.
Precomputed average ratings once (outside the loop).
Removed unnecessary copies and ad-hoc conversions; ensured the result is sorted by correlation.

Highlights:

Targeted normalization: only Book-Title and Book-Author are lowercased.
ISBN comparison uses a simple strip (no lowercasing) and matches the original ISBN column exactly.
Vectorized correlation:
Before: one-by-one correlation in a Python loop.
Now: dataset_for_corr.corrwith(dataset_for_corr[target_book_title]) for all columns at once.
Popularity threshold computed with groupby('Book-Title')['User-ID'].size() for speed.
Average ratings computed once via ratings_data_raw.groupby('Book-Title')['Book-Rating'].mean() and merged.
Output sorted by correlation descending.
```

Further optimization suggestions
```
Further optimizations you can consider
Cache the prepared dataset:
If you call find_correlated_books_by_isbn repeatedly, memoize prepare_dataset() (e.g., with functools.lru_cache(maxsize=1)) so the merge and normalization aren’t repeated each time.
Sparse matrices for large data:
Convert the pivot (user × book) to a sparse matrix and use cosine similarity (scikit-learn’s pairwise cosine_similarity on CSR) for speed and memory efficiency.
Precompute offline:
Build a precomputed item–item similarity matrix once (with a popularity floor), serialize it, and do O(1) lookups at runtime.
Reduce memory pressure:
Downcast integer columns (e.g., User-ID to int32) and consider categoricals for Book-Title if you keep doing merges/groupbys on it.
Better ISBN handling:
Normalize hyphens/whitespace once on load for both ratings and books (e.g., books['ISBN'] = books['ISBN'].str.replace('-', '').str.strip() and same for ratings) if your inputs vary in formatting.
```

### 2024-10-26
Experiments with grouping by ISBN resulted in not useful model because there's not enough data.
I choose to go back to grouping by Book-Title and accept inaccuracies.
Results of the model grouped by Book-Title look more useful.

Playing around with Docker for the CLI app.

Building Streamlit frontend

Note: fitering out the implicit ratings might exclude some books
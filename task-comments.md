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



**Fulltext ideas**

🧱 4. Using TF-IDF + cosine similarity (keyword ranking)

For “real” full-text search where you want ranking by relevance, use scikit-learn’s TfidfVectorizer:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

texts = df["text"].fillna("").tolist()
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(texts)

def search(query: str, top_k: int = 3):
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = scores.argsort()[::-1][:top_k]
    return df.iloc[top_indices], scores[top_indices]

result, scores = search("data python")
print(result)
print(scores)
```

✅ Pros:

ranked results

fast even for thousands of docs

supports weighting & stopwords
⚠️ Cons:

doesn’t understand meaning (purely keyword-based)

🧬 5. Semantic search (optional, for advanced use)

If you want semantic search (i.e., “find things similar in meaning, not just words”), you can use sentence embeddings via sentence-transformers (BERT-like models):

```python
from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(df["text"].tolist(), convert_to_tensor=True)

def semantic_search(query: str, top_k: int = 3):
    query_emb = model.encode(query, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_emb, embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    indices = top_results.indices.tolist()
    scores = top_results.values.tolist()
    return df.iloc[indices], scores

result, scores = semantic_search("programming in Python")
print(result)
print(scores)
```


✅ Pros:

captures meaning, not just words
⚠️ Cons:

slower, heavier (needs torch + transformer model)

overkill unless you need semantic similarity
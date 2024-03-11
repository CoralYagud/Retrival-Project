import nltk
from collections import defaultdict
from nltk.stem.porter import *
from nltk.corpus import stopwords
import numpy as np
from files import title_index, body_index, pagerank_dict, document_lengths, title_lengths, id_to_title_dict, train_dict

nltk.download('stopwords')
english_stopwords = frozenset(stopwords.words('english'))
corpus_stopwords = ["category", "references", "also", "external", "links",
                    "may", "first", "see", "history", "people", "one", "two",
                    "part", "thumb", "including", "second", "following",
                    "many", "however", "would", "became"]

all_stopwords = english_stopwords.union(corpus_stopwords)
RE_WORD = re.compile(r"""[\#\@\w](['\-]?\w){2,24}""", re.UNICODE)


def process_query(query):
    # Tokenize the query
    query_tokens = [token.group() for token in RE_WORD.finditer(query.lower())]

    # Remove stopwords from the query
    query_tokens = [token for token in query_tokens if token not in all_stopwords]

    return query_tokens


def tfidf_cal(tokens, index_body, index_title, folder_name, document_lengths, title_lengths, bucket_name = '209502079'):
    tf_body, idf_body = defaultdict(float), defaultdict(float)
    tf_title, idf_title = defaultdict(float), defaultdict(float)
    n = len(document_lengths)

    # Calculate TF-IDF for body
    for token in tokens:
        posting_list = index_body.read_a_posting_list(folder_name, token, bucket_name)
        tf_values = {}
        for doc_id, tf_val in posting_list:
            doc_length = document_lengths[doc_id]
            tf_values[doc_id] = tf_val / doc_length
        tf_body[token] = list(tf_values.items())
        df = len(posting_list)
        if df == 0:
          idf_body[token] = 0
        else:
          idf_body[token] = np.log10((n) / (df))

    # Calculate TF-IDF for title
    for token in tokens:
        posting_list = index_title.read_a_posting_list(folder_name, token, bucket_name)
        tf_values = {}
        for doc_id, tf_val in posting_list:
            doc_length = title_lengths[doc_id]
            tf_values[doc_id] = tf_val / doc_length
        tf_title[token] = list(tf_values.items())
        df = len(posting_list)
        if df == 0:
          idf_title[token] = 0
        else:
          idf_title[token] = np.log10((n) / (df))

    return tf_body, idf_body, tf_title, idf_title


def dot_product_similarity(query, index_body, index_title, folder_name, document_lengths, title_lengths, bucket_name):
    tf_body, idf_body, tf_title, idf_title = tfidf_cal(query, index_body, index_title, folder_name, document_lengths, title_lengths, bucket_name)
    tfidf_combined = defaultdict(float)

    # Calculate TF-IDF for body
    for token, idf_val in idf_body.items():
        for doc_id, tf_val in tf_body[token]:
            tfidf_combined[doc_id] += 0.2 * (tf_val * idf_val)  # 30% contribution from body

    # Calculate TF-IDF for title
    for token, idf_val in idf_title.items():
        for doc_id, tf_val in tf_title[token]:
            tfidf_combined[doc_id] += 0.8 * (tf_val * idf_val)  # 70% contribution from title

    return sorted(tfidf_combined.items(), key=lambda x: x[1], reverse=True)


def retrieval_function(query, index_body, index_title, folder_name, document_lengths, title_lengths, pagerank_scores, id_to_title_dict, bucket_name = '209502079'):
    # Calculate dot product similarity scores
    dot_product_scores = dot_product_similarity(query, index_body, index_title, folder_name, document_lengths, title_lengths, bucket_name)

    # Combine dot product similarity and PageRank scores
    combined_scores = defaultdict(float)
    for doc_id, dot_product_score in dot_product_scores:
        pagerank_score = pagerank_scores[doc_id]
        combined_scores[doc_id] = 0.7 * 10000 * dot_product_score + 0.3 * pagerank_score

    # Rank documents based on combined scores
    ranked_documents = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    # Retrieve up to 30 search results with titles
    search_results = []
    for doc_id, score in ranked_documents[:30]:
        title = id_to_title_dict.get(doc_id, "Title not available")
        search_results.append((str(doc_id), title))

    return search_results


def backend_search(query):
    # Process the query
    query = process_query(query)

    # Retrieve search results using the retrieval function
    search_results = retrieval_function(query, body_index, title_index, '.', document_lengths, title_lengths,
                                         pagerank_dict, id_to_title_dict, bucket_name='209502079')

    return search_results

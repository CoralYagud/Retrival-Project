# 📚 Retrival-Project

## Wikipedia Information Retrieval System

This repository contains the codebase for building an information retrieval system using data from Wikipedia.  
The system utilizes **inverted indexes**, **PageRank**, and ranking algorithms like **BM25** to provide relevant search results.

---

## 📁 Directory Structure

- **`backend_search_bm25/`**  
  Contains backend code for search functionality using the **BM25** ranking algorithm.

- **`backend_search/`**  
  Contains backend code for search functionality using the **Dot Product Similarity** ranking algorithm.

- **`files/`**  
  Sets up the necessary environment variables and loads various components for the search engine project from **Google Cloud Storage**.

- **`inverted_index_gcp/`**  
  Implementation of inverted index creation and management designed for use on **Google Cloud Platform (GCP)**.

- **`search_frontend/`**  
  Frontend code responsible for user interface components and interactions related to search functionality.

- **`Indexes_and_dictonaries_creation_gcp/`**  
  Contains scripts and code for creating and managing dictionaries and indexes on **Google Cloud Platform (GCP)**.

---

## 🧩 Components

### 🔎 Inverted Index

- **Body Index**:  
  Index built from the body of each Wikipedia page, excluding stopwords.  
  Tokenization, word counting, and posting list creation are performed to enable fast searching of content.

- **Title Index**:  
  Index built from document titles, filtering out rare words.  
  Titles often provide concise summaries of content, facilitating quick retrieval of relevant pages.

---

### 🔗 PageRank

PageRank scores are calculated based on page connectivity (anchor text) and stored in `pagerank_dict`.  
Integration of PageRank improves relevance of search results by prioritizing key pages in subject areas.

---

### 📖 Reference Dictionaries

- **`document_lengths`**:  
  Stores lengths of each document based on word count in the text body, aiding in ranking search results.

- **`title_lengths`**:  
  Similar to document lengths, stores title lengths of each document.

- **`id_to_title_dict`**:  
  Maps document IDs to corresponding titles, facilitating retrieval of document titles based on IDs.

---

## ⚙️ Ranking Functions

Two ranking functions, **BM25** and **Dot Product Similarity**, are implemented to evaluate effectiveness in information retrieval.  
BM25 is chosen for its ability to handle term frequency variations and sparse queries.

---

## 🔍 Query Processing and Retrieval

Queries are standardized similar to operations on indexes.  
Retrieval function uses the selected ranking function (**BM25** or **Dot Product Similarity**) and **PageRank** to determine final ranking and retrieve relevant pages.

---

## 📊 Experiments and Results

Evaluation is performed on the **train set** using the **BM25** ranking function.  
Results are analyzed based on:
- **Average Latency**
- **Average Quality of Results**
- **Precision Metrics**:  
  - `Precision@5`  
  - `Precision@10`  
  - `F1@30`

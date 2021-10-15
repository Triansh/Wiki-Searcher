# Wiki-Searcher

Wiki-Searcher is a search engine trained from a corpus of wikipedia articles to provide efficient
query results. The wikipedia dump comprised of nearly 20 million documents which corresponds to
approximately 80 GBs of data. The size of the created inverted index was ~17.5 GBs which was divided
into 3000 files containing indexes and titles. The index had ~10 million tokens from the corpus.

## Installation

* Ensure that you have python 3.8+ installed in your system. To create the environment and install
  dependencies, use the following set of commands.

```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

* To create the index, run the following commands. It requires the path to the dump which needs to
  be indexed, the path to directory where index is created and the path were statistics file will be
  written.

```shell
$ bash index.sh <path_to_dump> <path_to_index_directory> <path_to_stat_file>
```

* For searching, place the queries in queries.txt file present in the directory from the script is
  executed. The argument taken by script is the path where index is stored.

```shell
$ bash search.sh <path_to_index_directory> 
```

## Procedure

### Method for indexing

Files responsible for indexing

1. `indexer.py`: Responsible for XML parsing
2. `TextProcessor.py`: Responsible for text processing
3. `InvertedInder.py`: Responsible for creating index files and performing merge sort

<hr/>

Indexing is done in the following steps

* XML Parsing of dump
* Text Processing of documents
    * Field Extraction
    * Tokenization
    * Stop words removal
    * Stemming
* The specific number of tokens from a set of documents are stored with fields and frequency among
  various files
* Merge sort is performed to merge and sort the tokens alphabetically and are distributed in files.

### Method for searching

Files responsible for searching

1. `search.py`: Responsible for query processing and loading of index and titles
2. `Ranker.py`: Responsible for ranking and scoring using BM25

<hr/>

Searching is done in the following steps

* Data (Frequencey of documents) loading and Query parsing
* Word and field extraction
* Retrieval of posting list from index and filtering based on fields
* Scoring documents using BM25 algorithm
* Ranking based on score
* Retriving titles of highly scored documents
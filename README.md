# Wiki-Searcher

A search engine trained from a corpus of wikipedia articles to provide efficient query results.

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
$ bash index.sh <path_to_dump> <path_to_inverted_index_directory> <path_to_stat_file>
```
* To create the index run, the following commands. It requires the path to the dump which needs to
  be indexed, the path to directory where index is created and the path were statistics file will be
  written.
```shell
$ bash search.sh <path_to_inverted_index_directory> <query_file_path>
```

[comment]: <> (***Anykind of spacing in these***)

[comment]: <> (```angular2html)

[comment]: <> (Title)

[comment]: <> (<page>)

[comment]: <> (    <title></title>)

[comment]: <> (</page>)

[comment]: <> (```)

[comment]: <> (```angular2html)

[comment]: <> (Infobox)

[comment]: <> ({{Infobox)

[comment]: <> (```)

[comment]: <> (```angular2html)

[comment]: <> (References)

[comment]: <> (==References==)

[comment]: <> (== References ==)

[comment]: <> (```)

[comment]: <> (```angular2html)

[comment]: <> (Category)

[comment]: <> ([[Category)

[comment]: <> (```)

[comment]: <> (```angular2html)

[comment]: <> (Links)

[comment]: <> (== External links ==)

[comment]: <> (== links == )

```
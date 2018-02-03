# CS242 Information Retrieval & Web Search
## Winter 2018 
### Project

Using the Twitter Streaming API, collect tweets, index, and search utilizing Lucene. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

- [Python 3](https://www.python.org/download/releases/3.0/)

- [PyLucene](http://lucene.apache.org/pylucene/)

### Installing

Follow the installation instructions for Python and PyLucene 

## Running the tests

To run the full test execute the following command: 

```cmd
python3 main.py {options...}
```

With the supported `{options...}`

1. `--generateFile {outputFileName}`
2. `--file {inputFileName}`
3. `--search {searchTerm}`
4. `--searchTwitter {outputFileName}`
    - Queries Twitter for 10,000 teets returned for search term
5. `--skipIndex {true/false}`
    - Skips index generation if already exists
6. `--maxTweetCount {integer}`
    - Will only collect this number of tweets

Examples:
```cmd
python3 main.py --generateFile tweets.csv --search "Term1","Term2" --maxTweetCount 10000
```
```cmd
python3 main.py --file tweets.csv --skipIndex true --search "Term1"
```
## Authors

* **Trevor Van Meter** - GitHub: [vanmeter-t](https://github.com/vanmeter-t)


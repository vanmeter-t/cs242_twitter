# CS242 Information Retrieval & Web Search
## Winter 2018 
### Project

Using the Twitter Streaming API, collect tweets, index, and search utilizing Lucene. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

- [Python 3](https://www.python.org/download/releases/3.0/)

- [Tweepy](https://github.com/tweepy/tweepy)

- [PyLucene](http://lucene.apache.org/pylucene/)

### Installing

Follow the installation instructions for Python and PyLucene 

- Requires ant: $ sudo apt-get install ant

- Execute the following command to install and setup
```cmd
./installer.sh
```

**COMPLETE THE FOLLOWING FILE**

Twitter API Credentials need to be stored in the `private.py` file: as follows:
```
TWITTER_KEY = ""
TWITTER_SECRET = ""
TWITTER_APP_KEY = ""
TWITTER_APP_SECRET = ""
```

## Running the tests

To run the full test execute the following command: 

```cmd
python3 main.py {options...}
```

With the supported `{options...}`

- `--generateFile {outputFileName}`

- `--file {inputFileName}`

- `--searchIndex {searchTerm}`

- `--searchTwitter {outputFileName}`
    - Queries Twitter for 10,000 teets returned for search term

- `--skipIndex {true/false}`
    - Skips index generation if already exists

- `--maxTweetCount {integer}`
    - Will only collect this number of tweets

- `--customPhrase {customPhrases}`
    - Will customize the index for these specific phrases (i.e. "Hello World", "West Coast", etc.)

Examples:
```cmd
python3 main.py --generateFile tweets.csv --searchIndex "Term1","Term2" --maxTweetCount 10000
```
```cmd
python3 main.py --file tweets.csv --skipIndex true --searchIndex "Term1"
```
```cmd
 python3 main.py --file tweets2.csv --searchIndex "#WMPO" --customPhrases "PGA Tour","Rickie Fowler"
 ```
## Authors

* **Trevor Van Meter** - GitHub: [vanmeter-t](https://github.com/vanmeter-t)


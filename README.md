# Word Counter

This project counts the numer of ocurrencies of the words on a given text

## Installation

The project runs on Python 3.x so you will need to have Python installed. Here's the [link to download it](https://www.python.org/downloads/)

Also, you will need the following packages, you can install them by coping the following comands on your terminal
```bash
pip install flask
pip install requests
pip install re
pip install pandas
```

## Usage

Once everything is installed you will need to `cd` to the folder where the project files are.

Once you are located on the folder you need to run the following command in order to execute the program:
```bash
python wordCounter.py
```

This aplication has two endpoints:


### Word Counter
```bash
POST /word-counter
```
This one sents the words to be counted, you need to send the following body with the request:
```javascript
{
    "simpleString": "some value",
    "filePath": "some path",
    "dataUrl": "some url"
}
```


`simpleString` is just a basic string
`filePath` is the path to a txt file where the text to be counted is. I've added a file with 100 paragraphs of lorem ipsum for testing.
`dataUrl` is the url of a the page to be processed, the program strips all the html tags and leaves just the text.

**Important:** all the three parameters must be present, if you dont want to use one of them you can leave it as an empty string "". You can also send data in the tree fields.

Expected successfull response:
```javascript
{
    "message": "The words were successfully counted",
    "status": 200
}
```

### Word Statistics
```bash
GET /word-statistics
```
This endpoint number of appearances for every word. The words are stored in the `historicCount.csv` file.

If you want to receive the count of just one word you need to add the `?word=` as a parameter and you will receive the number of appearances of that specific word.

Expected successfull response:
```javascript
{
    "word1": 1,
    "word2": 3,
    "word3": 2
}
```
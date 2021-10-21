import flask
from flask import json
import requests
from flask import request, jsonify
import re
import pandas as pd

app = flask.Flask(__name__)


@app.route('/word-statistics', methods=['GET'])
def wordStatistics():
    
    word = request.args.get('word')
    
    data = pd.read_csv("./historicCount.csv",  index_col=0, squeeze=True).to_dict()
    
    if word:
        word = formatInput(word)
        data = data.get(word[0])

    res = jsonify(data)
    return res

@app.route('/word-counter', methods=['POST'])
def wordCounter():
    
    try:
        if len(request.json["simpleString"]) > 0:
            res = calculateWordCount(request.json["simpleString"])

        # Assumption:
        # For testing simplicity I'm assuming it will be a txt file
        # We could add support for pdf files using PyPDF2
        if len(request.json["filePath"]) > 0:
            with open(request.json["filePath"]) as textFile:
                for line in textFile:
                    res = calculateWordCount(line)

        # Assumption:
        # The response from the url is just plaint html
        # If you want to recover certain parts of the page a better strategy would be to use beautifulsoup and scrape all those texts
        if len(request.json["dataUrl"]) > 0:
            text = requests.get(request.json["dataUrl"]).content.decode('utf-8')
            res = calculateWordCount(text)
    
    except Exception as e:
        # Assumption:
        # You will always send the 3 request parameters they can be an empty string but the key has to be there
        res = jsonify({'status': 400, 'message': 'You must enter all the request parameters'})
    
    return res



def calculateWordCount(inputText):
    try:
        formattedInput = formatInput(inputText)

        #convert to a set in order to remove duplicates
        wordsSet = set(formattedInput)
        wordCount = []
        for word in wordsSet:
            wordCount.append(formattedInput.count(word))

        wordCountDictionary = pd.DataFrame({'Words': list(wordsSet),  'Appearances': wordCount})

        updateHistoricCount(wordCountDictionary)

        return jsonify({'status': 200, 'message': 'The words were successfully counted'})
    
    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)})

def formatInput(inputText):
    # remove all numbers and html tags before removing alphanumerics otherwise it will end with floating html words
    inputText = re.sub("[0-9]+", '', inputText)
    inputText = re.sub('<.*?>', '',inputText)
    inputText = inputText.replace("\n",'')
    inputText = inputText.replace("\r",' ')

    #remove all non-alphanumeric chars
    inputText = re.sub(r'\W+', ' ', inputText)

    inputText = inputText.strip()
    inputText = re.sub(" +", ' ', inputText)
    
    inputText = inputText.upper()
    return inputText.split(' ')

def updateHistoricCount(wordDataframe):
    historicValues = pd.read_csv("./historicCount.csv")
    historicValues = pd.concat([historicValues, wordDataframe]).groupby(by=['Words']).sum()
    historicValues.to_csv("./historicCount.csv")

if __name__ == '__main__':
    app.run(debug=True, port= 8080)
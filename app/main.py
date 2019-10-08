from bs4 import BeautifulSoup
import requests
import json
import datetime
from dateutil.parser import parse
import os
from flask import Flask, render_template, jsonify
app = Flask(__name__)

def getHtml():
    headers = {'User-Agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
               'Referer': 'https://themetphilly.com/events/'}

    r = requests.get("https://themetphilly.com/events/", headers=headers)

    data = r.text

    with open('test.txt', 'w+') as f:
        f.write(data)


def createJson():

    getHtml()

    with open("test.txt",'r+') as f:
        data = f.read()

    myDict = {}
    date = ''
    name = ''
    soup = BeautifulSoup(data , features="lxml")
    myList = soup.find_all('div', "event-item-info")
    jsonList = []
    for i in myList:
        for j in i.contents:
            if j != "\n":
                if j.name == 'h3':
                    date = parse(j.contents[0]).strftime('%b %d %Y')
                if j.name == 'h1':
                   name = j.contents[0]

        myDict["Date"]=date
        myDict["Name"]=name
        jsonList.append(myDict)
        jsonList.sort(key = lambda date: datetime.datetime.strptime(date["Date"], '%b %d %Y'))
        # print(myDict)
        myDict = {}
    newDict={}
    newDict["data"]=jsonList
    myJson = jsonify(newDict)
    return myJson

def checkEvent(obj):
    today = datetime.date.today()
    returnString = 'no event today'
    for i in obj:
        if today == parse(i).date():
            returnString = "there is an event today. "+ obj[i]+" is playing."

    return returnString


@app.route("/today")
def main():
    jsonObj = createJson()
    return checkEvent(json.loads(jsonObj))

@app.route("/events")
def events():
    jsonObj = createJson()
    return jsonObj

@app.route('/index')
@app.route('/')
def index():
  return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', debug=True, port=port)

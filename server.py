from flask import Flask
from flask import request
from flask.ext import restful
from pymongo import MongoClient
from datetime import datetime
import json


#Standard MongoDB Format
#article../ lastaccess: string, title: string, author: string, pubdate: string,
#description: string, url: string, imageurl: array<string>, read: int, rsstitle: string
#rss../ url: string, title: string, test: string
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
time = datetime.now()
time = time.strftime(DATETIME_FORMAT)
time = str(time)
app = Flask('rss')
client = MongoClient()
db = client.rssdb
article = db.article
rss = db.rss

@app.route("/", methods=['GET', 'POST'])
def subscribe():
	test = request.json
	print test
	look = rss.find_one({"url": test['url']},{"_id": 0})
	if look is None:
		rss.insert(test)
		return "1"
	else:
		return "0"

@app.route("/read/<name>")
def getArticle(name):
	if look is None:
		look = article.find_one({"url": name},{"lastaccess": 0, "title": 0, "author": 0, "pubdate": 0, "description": 0, "url": 0, "imageurl": 0, "read": 0, "rsstitle": 0})
		db.article.update(look, {"read": 1})
		return "1"
	else:
		return "0"
@app.route("/pull/<writer>")
def pull(writer):
	text = ""
	fullarticle = article.find({"author": writer}, {"_id": 0})
	for story in fullarticle:
		text += "<p>"+story['description']+"</p>" +"<p>"+"<a href=>"+ story['url']+">Link text</a>" +" </p>" +"<br><br>"
	return text
@app.route("/pullfeed")
def feed():
	array = []
	fullfeed = rss.find({"test": "set"},{"_id": 0})
	for feed in fullfeed:
		array.append(json.dumps(feed))
	end = ''.join(array)
	return end
app.run(host='192.81.208.114')

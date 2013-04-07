from flask import Flask
from flask.ext import restful
from pymongo import MongoClient
from datetime import datetime
import json


#Standard MongoDB Format
#article../ lastaccess: string, title: string, author: string, pubdate: string,
#description: string, url: string, imageurl: array<string>, read: int, rsstitle: string
#rss../ url: string, title: strig
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
time = datetime.now()
time = time.strftime(DATETIME_FORMAT)
time = str(time)
app = Flask('rss')
client = MongoClient()
db = client.rssdb
article = db.article
rss = db.rss
@app.route("/")
def hello():
	return "hello"
@app.route("/url/<website>/title/<webtitle>")
def subscribe(website, webtitle):
	
	look = rss.find_one({"url": website},{"_id": 0})
	if look is None:
		sub = { "url": website, "title": webtitle}
		rss.insert(sub)
		return "1"
	else:
		return "0"

@app.route("/read/<name>")
def read (name):
	look = article.find_one({"url": name},{"_id": 0})
	if look is None:
		look = article.find_one({"url": name},{"lastaccess": 0, "title": 0, "author": 0, "pubdate": 0, "description": 0, "url": 0, "imageurl": 0, "read": 0, "rsstitle": 0})
		db.article.update(look, {"read": 1})
		return "1"
	else:
		return "0"
@app.route("/pull/<link>")
def pull(link):
	array = []
	fullarticle = article.find({"url": link}, {"_id": 0})
	for art in fullarticle:
		array.append(art)
	end = ''.join(array)
	return end
@app.route("/pullfeed")
def feed():
	array = []
	fullfeed = rss.find({"_id": 0})
	for feed in fullfeed:
		array.append(feed)
	end = ''.join(array)
	return end
app.run()

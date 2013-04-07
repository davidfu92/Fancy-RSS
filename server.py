from flask import Flask
from flask.ext import restful
from pymongo import MongoClient
from datetime import datetime
import json

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
time = datetime.now()
time = time.strftime(DATETIME_FORMAT)
time = str(time)
app = Flask('rss')
@app.route("/")
def hello():
	client = MongoClient()
	db = client.rssdb
	post = {"Title": "RSS", "Date": time}
	posts = db.posts
	post_id = posts.insert(post)
	for info in posts.find({"Title": "RSS"}):
		print info
	name = posts.find_one({"Title": "RSS"},{"_id": 0})
	out = json.dumps(name) + "\n"
	return out
app.run()


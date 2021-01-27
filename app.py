from flask import Flask, escape, url_for
from flask_pymongo import PyMongo
import requests
import json,re,os
def to_dict(movie):
    movie = movie.replace(' ','').replace(',','').replace('链接：','').replace('链接:','')
    link = re.findall(r'https?://[^\s]+', movie)
    link = link[0] 
    movie = movie.replace(link,' '+link)
    res = movie.split(' ')
    return {
            "movie":res[0],
            "link":res[1]
            }

app = Flask(__name__)
movies = requests.get("https://k2f1.cn/a/all_aptx4869").json()['data']
mongo = PyMongo(app,uri="mongodb+srv://daniel:zD199727@cluster0.nbfqb.mongodb.net/demo?retryWrites=true&w=majority")
for index,movie in enumerate(movies):
    movies[index] = movie.replace(' ','').replace(',','').replace('链接：','').replace('链接:','')
    if len(movies[index].split("：")) is not  3:
        movies.remove(movies[index])
    link = re.findall(r'https?://[^\s]+', movie)
    if len(link) < 1:
        movies.remove(movies[index])
res = list(map(to_dict,movies))
mongo.db.user.delete_many({})
mongo.db.user.insert_many(res)
@app.route('/<int:page>')
def index(page):
    r = []
    for item in mongo.db.user.find({},{"_id":0}).limit(page):
        r.append(item)
    return json.dumps(r)
port = int(os.environ.get('PORT', 5000))
app.run(debug=False,port=port,host='0.0.0.0')

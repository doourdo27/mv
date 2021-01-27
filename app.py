from flask import Flask, escape, url_for
from flask_pymongo import PyMongo
import requests
import json,re,os
from flask_apscheduler import APScheduler
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
mongo = PyMongo(app,uri="mongodb+srv://daniel:zD199727@cluster0.nbfqb.mongodb.net/demo?retryWrites=true&w=majority")
def renew():
    global mongo
    movies = requests.get("https://k2f1.cn/a/all_aptx4869").json()['data']
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
    print("renew!! ")

@app.route('/new/')
def new():
    renew()
    return 'success'
@app.route('/<int:page>')
def index(page):
    r = []
    for item in mongo.db.user.find({},{"_id":0}).limit(page):
        r.append(item)
    return json.dumps(r)
renew()
scheduler = APScheduler()
scheduler.init_app(app=app)
scheduler.start()
scheduler.add_job(func=renew,id="1",trigger='interval', hours=1, replace_existing=True)
port = int(os.environ.get('PORT', 5000))
app.run(debug=False,port=port,host='0.0.0.0')

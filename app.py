from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.newsdb

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

# API 역할을 하는 부분
@app.route('/article', methods=['GET'])
def show_articles():
    news = list(db.news.find({},{'_id':False}).sort('company_name',1))
    return jsonify({'all_news': news})

@app.route('/article/views', methods=['GET'])
def show_topArticles():
    top_views = list(db.allnews.find({},{'_id':False}).sort('view',-1).limit(5))
    return jsonify({'top_views': top_views})

@app.route('/article/views', methods=['POST'])
def view_article():
    url_receive = request.form['article_url']
    print(url_receive)
    target_views = db.allnews.find_one({'article_url':url_receive})
    current_views = target_views['view']

    new_views = current_views + 1

    db.allnews.update_one({'article_url':url_receive},{'$set':{'view':new_views}})
    return jsonify({'msg': '좋아요 완료'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    name_receive = request.form['name_give']
    db.mystar.delete_one({'name':name_receive})
    return jsonify({'msg': '삭제 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
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
    bookmark = list(db.bookmark.find({},{'_id':False}))
    return jsonify({'all_news': news,
                    'bookmark':bookmark})

@app.route('/article/views', methods=['GET'])
def show_topArticles():
    top_views = list(db.allnews.find({},{'_id':False}).sort('view',-1).limit(5))
    return jsonify({'top_views': top_views})

@app.route('/article/headline', methods=['GET'])
def show_headlineArticles():
    haedline_news = list(db.headlinenews.find({},{'_id':False}))
    return jsonify({'haedline_news': haedline_news})

@app.route('/article/views', methods=['POST'])
def view_article():
    url_receive = request.form['article_url']
    target_views = db.allnews.find_one({'article_url':url_receive})
    current_views = target_views['view']

    new_views = current_views + 1

    db.allnews.update_one({'article_url':url_receive},{'$set':{'view':new_views}})
    return jsonify({'msg': '좋아요 완료'})

@app.route('/bookmark', methods=['GET'])
def get_bookmark():
    bookmarks = list(db.bookmark.find({},{'_id':False}))
    bookmark_news = []

    for bookmark in bookmarks:
        name = bookmark['company_name']
        bookmark_news = bookmark_news + list(db.news.find({'company_name': name},{'_id':False}).sort('company_name',1))
    return jsonify({'bookmark': bookmark_news})

@app.route('/bookmark', methods=['POST'])
def bookmark_company():
    company_receive = request.form['company_name']
    if(db.bookmark.find({'company_name':company_receive}).count() == 0):
        doc = {
            'company_name':company_receive
        }
        db.bookmark.insert_one(doc)
        return jsonify({'msg': '즐겨찾기 추가완료'})
    else:
        db.bookmark.delete_one({'company_name':company_receive})
        return jsonify({'msg': '즐겨찾기 삭제완료'})

@app.route('/api/delete', methods=['POST'])
def delete_star():
    name_receive = request.form['name_give']
    db.mystar.delete_one({'name':name_receive})
    return jsonify({'msg': '삭제 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
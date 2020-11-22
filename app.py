from flask import Flask, render_template, jsonify, request
import requests
# from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.dbglass



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/glassin', methods=['POST'])
def post_glass():
    searching = request.form['search_input']

    db.glasses.drop()

    client_id = '3cM33RVzsCGd7lI0ZmCU'
    client_secret = 'KoezOPz8XR'

    url = "https://openapi.naver.com/v1/search/image?query={}&display=30".format(searching)
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
    contents = requests.get(url, headers=headers).json()['items']

    for style in contents:
        style_url = style['thumbnail']
        img_url = style['link']

        doc = {

            'style_url': style_url,
            'img_url': img_url

        }

        db.glasses.insert_one(doc)

    return jsonify({'result': 'success'})


@app.route('/glassout', methods=['GET'])
def read_glass():
    glass_styles = list(db.glasses.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'styles': glass_styles})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

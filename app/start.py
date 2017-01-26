import json

from flask import Flask, jsonify
from flask import redirect
import xmltodict
from flask import render_template
from flask import session
from flask import url_for
from flask.ext.socketio import SocketIO
from flask_session import Session
from settings import *

from oauth import OAuthGoodreads

app = Flask(__name__)
app.config.from_object('settings')
Session(app)
socketio = SocketIO(app)

goodreads =OAuthGoodreads()

@app.route('/')
def rot():
    return render_template("index.html", title='Projects')


@app.route('/login')
def login():
    session['request_token'], session['request_token_secret'] = goodreads.generate_token()
    return redirect(goodreads.get_redirect_url(session['request_token']))


@app.route('/yaydone')
def gettoken():
    return redirect('/wc')

@app.route('/wc')
def loops():
    if 'request_token' not in session:
        return redirect(url_for('login'))
    if 'token' not in session:
        gr = goodreads.get_session(session['request_token'], session['request_token_secret'])
        session['token'] = (gr.access_token,gr.access_token_secret)
    else:
        gr = goodreads.get_session_with_token(session['token'])

    if 'user_id' not in session:
        data  = xmltodict.parse(gr.get('https://www.goodreads.com/api/auth_user').text)
        session['user_id'] = data["GoodreadsResponse"]["user"]["@id"]
    if 'review_data' not in session:
        data =xmltodict.parse(gr.get('https://www.goodreads.com/review/list.xml?shelf=read&v=2&id=' + str(session['user_id']) + '&per_page=200').text)
        session['review_data'] = data
    else:
        data = session['review_data']
    res = []
    for book in data['GoodreadsResponse']['reviews']['review']:
       read_at = (book['read_at'] if book['read_at'] != None else book['date_added'] )
       read_at = read_at[:10] + ' ' + read_at[-4:]
       num_pages = book['book']['num_pages']
       res.append({ 'date' : read_at , 'num_pages' : num_pages})
    return jsonify(res)
    #payload = { 'shelf' : 'read'  , 'v' : 2 , 'per_page' : 200,  }
    #data = session.get('https://www.goodreads.com/review/list')

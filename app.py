from flask import Flask, render_template, redirect, url_for
import sqlite3

dbname = 'shichigo.db'
conx = sqlite3.connect(dbname)

app = Flask(__name__)

# ページルーティング
@app.route('/')
def redirect_index():
    return redirect(url_for('compose'))

@app.route('/compose')
def compose():
    return render_template('compose.jinja.html')

# APIルーティング
@app.route('/shichigo', methods=['GET', 'POST'])
def shichigo():
    # if request.method == 'POST':
        # cur = conx.cursor()
        # cur.execute('INSERT INTO shichigo PARAM')
    return ''
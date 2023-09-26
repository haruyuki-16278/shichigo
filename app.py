from flask import Flask, render_template, redirect, url_for
import sqlite3

dbname = 'shichigo.db'
conx = sqlite3.connect(dbname)

app = Flask(__name__)

# ページルーティング
@app.route('/')
def page_redirect_index():
    return redirect(url_for('page_compose'))

@app.route('/compose')
def page_compose():
    return render_template('compose.jinja.html')

@app.route('/appreciation')
def page_read():
    return render_template('appreciation.jinja.html')

# APIルーティング
@app.route('/shichigo', methods=['GET', 'POST'])
def shichigo():
    # if request.method == 'POST':
        # cur = conx.cursor()
        # cur.execute('INSERT INTO shichigo PARAM')
    return ''

app.run('0.0.0.0', 5000, True, False)
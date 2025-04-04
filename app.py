import sqlite3
from flask import Flask, render_template, request, redirect
import random, string

# Flask app
app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect("my_urls.db", check_same_thread=False)
    connection.row_factory = sqlite3.Row  # To access columns by name
    return connection

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    longurl = request.form['longurl']
    connection = get_db_connection()
    cursor = connection.cursor()

    sql = "SELECT * FROM urls WHERE long_url = ?"
    cursor.execute(sql, (longurl,))
    results = cursor.fetchall()

    if results:
        shorturl = results[0]['short_url']  # if its already in the database then we can simply access it
    else:
        shorturl = short_url_generator()
        insertion = "INSERT INTO urls (long_url, short_url) VALUES (?, ?)" # if not already in database, we insert it
        cursor.execute(insertion, (longurl, shorturl))
        connection.commit()

    connection.close()
    return render_template('index.html', shorturl=request.host_url + shorturl, longurl=longurl)

@app.route("/<short_url>")
def redirect_to_long(short_url):
    connection = get_db_connection()
    cursor = connection.cursor()

    sql = "SELECT long_url FROM urls WHERE short_url = ?"
    cursor.execute(sql, (short_url,))
    result = cursor.fetchone()

    connection.close()

    if result:
        return redirect(result['long_url'])
    else:
        return render_template('error.html', message="Short URL not found")

def short_url_generator():
    letters = string.ascii_lowercase
    x = ''.join(random.choice(letters) for i in range(4))
    return x  # return short part

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template
import pymysql
from datetime import datetime

app = Flask(__name__)

conn = pymysql.connect(host='localhost', user='flaskuser', password='flaskpass', db='notesdb')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form['note']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with conn.cursor() as cur:
            cur.execute("INSERT INTO notes (note, timestamp) VALUES (%s, %s)", (note, timestamp))
            conn.commit()
    with conn.cursor() as cur:
        cur.execute("SELECT note, timestamp FROM notes ORDER BY id DESC")
        notes = cur.fetchall()
    return render_template('index.html', notes=notes)

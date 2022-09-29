from operator import methodcaller
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_mysqldb import MySQL
import mysql
import MySQLdb.cursors

app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'random'


@app.route('/', methods=['GET', 'POST'])
def home():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM random")
    random = cur.fetchall()
    if request.method == "POST" and "random-title" in request.form and "random-desc" in request.form:
        title = request.form.get("random-title")
        desc = request.form.get("random-desc")
        cur.execute("INSERT INTO random VALUES(NULL, %s, %s)", (title, desc))
        mysql.connection.commit()
        return redirect('/')
    return render_template("index.html", random = random)

@app.route('/random/<int:id>')
def random(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM random")
    random = cur.fetchall()[id]
    return render_template('random.html',random = random, id = id)

if __name__ == "__main__":
    app.run(debug=True)
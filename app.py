from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__) #flask server configuration
Bootstrap(app) #bootstrap initialization

#Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html', tareas = db_query("select * from tareas"))

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        desc = request.form['tarea']
        fecha_limite = request.form['fecha_limite']
        query = "INSERT INTO tareas(descripcion, fecha_creacion, fecha_limite) " \
                "VALUES ('{}', '{}', '{}')".format(desc, datetime.datetime.now(), fecha_limite)
        db_modification(query)
        return redirect(url_for('index'))


@app.route('/remove/<int:id>')
def remove(id):
    query = "DELETE FROM tareas WHERE id = {}".format(id)
    db_modification(query)
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    if request.method == "GET":
        query = "SELECT * FROM tareas WHERE id = {}".format(id)
        tarea = db_query(query)
        return render_template('edit.html', tarea = tarea)

    if request.method == "POST":
        desc = request.form['tarea']
        fecha_limite = request.form['fecha_limite']
        query = "UPDATE tareas SET descripcion = '{}', fecha_limite = '{}' WHERE id = {}".format(desc, fecha_limite, id)
        db_modification(query)

        return redirect(url_for('index'))


def db_query(query):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute(query)

    return cursor.fetchall()

def db_modification(query):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
if __name__ == '__main__':
    app.run()

from flask import *
import mysql.connector
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="masker")

cursor = mydb.cursor()

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/aksi_login', methods = ["POST", "GET"])
def aksi_login():
    cursor = mydb.cursor()
    query = ("select * from user where username = %s and password = md5(%s)")
    data = (request.form['username'], request.form['password'],)
    cursor.execute( query, data )
    value = cursor.fetchone()

    username = request.form['username']
    if value:
        session["user"] = username
        return redirect(url_for('tampil'))
    else:
        return f"salah!!!"
    
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route('/admin')
def admin():
    if session.get("user"):
        return render_template("admin.html")
    else:
        return redirect(url_for("login"))

@app.route('/simpan', methods = ["POST", "GET"] )
def simpan():
    jenis = request.form["jenis"]
    warna = request.form["warna"]
    fungsi = request.form["fungsi"]
    harga = request.form["harga"]
    query = ("insert into db_masker values( %s, %s, %s, %s, %s)")
    data = ( "", jenis, warna, fungsi, harga )
    cursor.execute( query, data )
    mydb.commit()
    cursor.close()
    return f"sukses disimpan.."

@app.route('/tampil')
def tampil():
    cursor = mydb.cursor()
    cursor.execute("select * from db_masker")
    data = cursor.fetchall()
    cursor.close()
    return render_template('tampil.html',data=data) 

@app.route('/hapus/<id>')
def hapus(id):
    cursor = mysql.connection.cursor()
    query = ("delete from db_masker where id = %s")
    data = (id,)
    cursor.execute( query, data )
    mysql.connection.commit()
    cursor.close()
    return redirect('/tampil.html')

@app.route('/update/<id>')
def update(id):
    cursor = mysql.connection.cursor()
    sql = ("select * from db_masker where id = %s")
    data = (id,)
    cursor.execute( sql, data )
    value = cursor.fetchone()
    return render_template('update.html',value=value) 


@app.route('/aksiupdate', methods = ["POST", "GET"] )
def aksiupdate():
    id = request.form["id"]
    jenis = request.form["jenis"]
    warna = request.form["warna"]
    fungsi = request.form["fungsi"]
    harga = request.form["harga"]
    cursor = mysql.connection.cursor()
    query = ("update db_masker set jenis = %s, warna = %s, fungsi = %s, harga = %s where id = %s")
    data = ( jenis, warna, fungsi, harga, id, )
    cursor.execute( query, data )
    mysql.connection.commit()
    cursor.close()
    return redirect('/tampil')

if __name__ == "__main__":
    app.run(debug=True)
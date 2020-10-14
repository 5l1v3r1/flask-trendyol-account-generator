from flask import Flask,flash,render_template,redirect,url_for,session,request
from forms import registerform,loginform
from functools import wraps #login required
from flask_mysqldb import MySQL
from bot import creater

__version__ = "1.0"

app = Flask(__name__)
app.secret_key = "notrustly1"
app.config["MYSQL_HOST"] = "yapayyazilim.mooo.com"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "notrustly1"
app.config["MYSQL_DB"] = "trendyolbot"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            if session["logged_in"]:
                return f(*args,**kwargs)
            else:
                flash("Önce giriş yapmalısınız","danger bg-warning")
                return redirect(url_for("login"))
        else:
            flash("Önce giriş yapmalısınız","danger bg-warning")
            return redirect(url_for("login"))
    return decorated_function



@app.route("/")
def index():
    global __version__
    return render_template("index.html",version=__version__)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Başarıyla çıkış yapıldı","success")
    return redirect(url_for("index"))

def get_process():
    cursor = mysql.connection.cursor()
    cursor.execute("select can_process from accounts where ID=%s", (session["ID"],))
    can_process = cursor.fetchone()["can_process"]
    cursor.close()
    return int(can_process)

def set_process(value):
    cursor = mysql.connection.cursor()
    cursor.execute("update accounts set can_process = %s where ID=%s",(int(value),session["ID"],))
    mysql.connection.commit()
    cursor.close()

def get_password():
    cursor = mysql.connection.cursor()
    cursor.execute("select mailspassword from accounts where ID=%s",(session["ID"],))
    psw = cursor.fetchone()["mailspassword"]
    return psw

def calistir():
    pas = get_password()
    username = session["username"]
    myid = session["ID"]
    creater(id=myid,username=username,password=pas)
    print(get_password())
    print(get_process())

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        result = cursor.execute("select Mail from mails where ID=%s",(session["ID"],))
        if result>0:
            data = cursor.fetchall()
            cursor.close()
            if get_process() == 1:
                calistir()
                set_process(0)
                return redirect(url_for("controlpanel",can_process = 0,data=data))
            else:
                return redirect(url_for("controlpanel",can_process = 0,data=data))
        else:
            cursor.close()
            if get_process() == 1:
                calistir()
                set_process(0)
                return redirect(url_for("controlpanel",can_process = 0))
            else:
                return redirect(url_for("controlpanel",can_process = 0))
    else:
        return redirect(url_for("controlpanel"))

@app.route("/controlpanel")
@login_required
def controlpanel():
    cursor = mysql.connection.cursor()
    cursor.execute("select can_process from accounts where id=%s",(session["ID"],))
    can_process = cursor.fetchone()["can_process"]
    result = cursor.execute("select Mail from mails where OwnerID=%s",(session["ID"],))
    if result>0:
        data = cursor.fetchall()
        cursor.close()
        return render_template("controlpanel.html",can_process=can_process,data=data)
    else:
        cursor.close()
        return render_template("controlpanel.html",can_process=can_process)


@app.route("/login",methods=["GET","POST"])
def login():
    form = loginform(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        cursor = mysql.connection.cursor()
        sql = "select * from accounts where username = %s"
        result = cursor.execute(sql,(username,))
        if result > 0:
            data = cursor.fetchone()
            if password == data["password"]:
                session["logged_in"] = True
                session["username"] = username
                session["ID"] = data["ID"]
                flash("Giriş başarılı","success")
                return redirect(url_for("index"))
            else:
                flash("Yanlış parola","danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kayıt bulunamadı","danger")
            return  redirect(url_for("login"))
    else:
        return render_template("login.html",form = form)

@app.route("/register",methods=["GET","POST"])
def register():
    form = registerform(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        MailPassword = form.MailsPassword.data
        cursor = mysql.connection.cursor()
        sql = "select * from accounts where username=%s"
        result = cursor.execute(sql,(username,))
        if result > 0:
            flash("Bu kullanıcı ismi zaten kayıtlı","danger")
            return  redirect(url_for("login"))
        else:
            sql = "insert into accounts(username,password,mailspassword) values(%s,%s,%s)"
            cursor.execute(sql,(username,password,MailPassword))
            mysql.connection.commit()
            sql = "select * from accounts where username = %s"
            cursor.execute(sql,(username,))
            data = cursor.fetchone()
            cursor.close()
            flash(f"Kayıt başarılı. Hoşgeldin {username}","success")
            session["logged_in"]=True
            session["username"]=username
            session["ID"] = data["ID"]
            return redirect(url_for("index"))
    else:
        return  render_template("register.html",form=form)

if __name__ == "__main__":
    app.run(debug=True,host="192.168.1.32",port=80)
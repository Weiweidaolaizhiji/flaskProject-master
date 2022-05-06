import json
import os

from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import jinja2
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "mysql://root:root@127.0.0.1:3306/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.INTEGER,primary_key=True)
    name = db.Column(db.String(16),unique=True)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER,primary_key=True)
    name = db.Column(db.String(16),unique=False)
    role_id = db.Column(db.INTEGER,db.ForeignKey('roles.id'))




ss = []
# with open('students.txt', 'r',encoding='utf-8') as file:
#     i = file.readlines()
#     for n in i:
#         rs = n.rstrip("\n")
#         ss.append(eval(rs))
#     print(ss)
#     file.close()

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


# 验证是否连接成功
@app.route('/')
def hello_word():
    engine = db.get_engine()
    conn = engine.connect()
    with engine.connect() as conn:
        result = conn.execute('select 1')  #这两步打开数据库并且创建表
        print (result.fetchone()) #打印一条数据
    conn.close() #跟open函数一样，可以用with语句
    return "hello, word"


@app.route('/login',methods=['GET','POST'])
def login():  # put application's code here
    if request.method =='POST':
        username = request.form.get("username")
        password = request.form.get("password")
        print(username,password)
        return redirect('admin')
    return render_template("login.html")

@app.route('/admin')
def admin():  # put application's code here
    return render_template("admin.html",students=ss)

@app.route('/add',methods=['GET','POST'])
def add():  # put application's code here
    if request.method =='POST':
        username = request.form.get("username")
        chinese = request.form.get("chinese")
        math = request.form.get("math")
        english = request.form.get("english")
        new_stu = {'name':username,'chinese':chinese,'math':math,'english':english}
        ss.append(new_stu)
        with open("students.txt", "a", encoding='utf-8') as f:
            f.write(json.dumps(new_stu,ensure_ascii=False)+"\n")
            f.close()
        return redirect('/admin')
    return render_template("add.html")

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method =="POST":
        ip = request.form.get("ip")
        username = request.form.get("username")
        password = request.form.get("password")
        user_info = {"ip":ip,"username":username,"password":password}
        with open('user.txt','a',encoding='utf-8') as f:
            f.write(json.dumps(user_info,ensure_ascii=False)+"\n")
            f.close()
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.abspath('./static/up_file')+"\\"+uploaded_file.filename)
            return render_template("update_verify.html",user_ip=ip)
    return render_template('upfile.html')

@app.route('/start_update')
def start_update():  # put application's code here
    return render_template("start_udate.html")



@app.route('/change',methods=['GET','POST'])
def change():  # put application's code here
    username = request.args.get('name')
    print(username)
    if request.method == "POST":
        username = request.form.get("username")
        chinese = request.form.get("chinese")
        math = request.form.get("math")
        english = request.form.get("english")
        for stu in ss:
            if stu.get('name') == username:
                stu['chinese'] = chinese
                stu['math'] = math
                stu['english'] = english
            return redirect('/admin')
    for i in ss:
        if i.get('name') == username:
            return render_template("change.html",students=i)

@app.route('/delete')
def delete():  # put application's code here
    username = request.args.get('name')
    print(username)
    for i in ss:
        if i['name'] == username:
            ss.remove(i)
    return redirect("/admin")

db.drop_all()
db.create_all()
role = Role(name='admin')
db.session.add(role)
db.session.commit()
if __name__ == '__main__':
    app.run()

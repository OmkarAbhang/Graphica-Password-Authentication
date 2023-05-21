from flask import Flask, render_template, request
from database import engine
from sqlalchemy import text
from passlib.hash import sha256_crypt

# creating object of flask
app = Flask(__name__)


@app.route("/")
def hello_world():
  return render_template("index.html")

@app.route("/SignUp")
def SignUp():
  return render_template("register.html")

@app.route("/SignIn")
def SignIn():
  return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
  email = request.form['email']
  name = request.form['name']
  textPwd = request.form['TextPwd']
  cnfPwd = request.form['CnfPwd']

  if textPwd != cnfPwd:
    error = "Password not matching!"
    return render_template("register.html", error=error)
  
  textPwd = sha256_crypt.encrypt(textPwd)
  password = '+'.join(request.form.getlist('imgPwd'))
  pwd = ""
  for i in range(len(password)):
    if password[i] != ',':
      pwd += password[i]
  pwd = sha256_crypt.encrypt(pwd)

  with engine.connect() as conn:
    checkQuery = "SELECT email FROM Users WHERE email = :email"
    if bool(conn.execute(text(checkQuery), {'email': email}).first()):
        error = "Email Id exists in the database."
        return render_template("register.html", error = error)
    
    query = "INSERT INTO Users (username, password, TextPwd, email) VALUES (:name, :pwd, :textPwd, :email)"
    conn.execute(text(query), {'name': name, 'pwd': pwd, 'textPwd':textPwd, 'email': email})

  return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    email = request.form['email']
    password = '+'.join(request.form.getlist('password'))
    pwd = ""
    for i in range(len(password)):
      if password[i] != ',':
        pwd += password[i]
    with engine.connect() as conn:
      queryUser = "SELECT * FROM Users WHERE email = :email"
      data = conn.execute(text(queryUser),{'email': request.form['email']}).fetchone()
      password = '+'.join(request.form.getlist('imgPwd'))
      pwd = ""
      for i in range(len(password)):
        if password[i] != ',':
          pwd += password[i]
      name = data[1]
      hashGraPwd = data[2]
      hashTxtPwd = data[3]
      if sha256_crypt.verify(request.form['TextPwd'], hashTxtPwd) and sha256_crypt.verify(pwd, hashGraPwd):
          return render_template('user.html', name=name)
      else:
          error = 'Invalid email or password'
          return render_template('login.html', error=error)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=False)

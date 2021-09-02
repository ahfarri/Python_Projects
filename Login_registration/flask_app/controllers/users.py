from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/create/user", methods=['POST'])
def create_user():
    if User.validate_user(request.form):

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        new_user = User.create(data)
        session['user_id'] = new_user
        return redirect("/success")
    return redirect('/')

@app.route("/login/user", methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"],
        "password" : request.form["password"] 
    }
    print("hello")
    user_db = User.get_user_email(data)
    print("hello")
    print(user_db)
    if not user_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_db.password,request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = user_db.id
    return redirect('/success')

@app.route('/success')
def register():
    if 'user_id' not in session:
        flash('You are not signed in. Please login.')
        return redirect('/')
    return render_template('success.html')

@app.route('/logout')
def logout():
    print(session)
    session.clear()
    print(session)
    return redirect("/")


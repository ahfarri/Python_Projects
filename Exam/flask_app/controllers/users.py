from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.car import Car
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
        return redirect("/dashboard")
    return redirect('/')

@app.route("/login/user", methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"],
        "password" : request.form["password"] 
    }
    user_db = User.get_user_email(data)
    print(user_db)
    user_ab = user_db[0]
    print(user_ab)
    if not user_ab:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_ab.password,request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_ab.id
    session['user_name'] =user_ab.first_name
    return redirect('/dashboard')

@app.route('/dashboard')
def register():
    if 'user_id' not in session:
        flash('You are not signed in. Please login.')
        return redirect('/')
    all_cars = Car.get_cars()
    return render_template('success.html', all_cars = all_cars)

@app.route('/logout')
def logout():
    print(session)
    session.clear()
    print(session)
    return redirect("/")



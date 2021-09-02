from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.car import Car
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/new')
def add_car():
    if 'user_id' not in session:
        flash('You are not signed in. Please login.')
        return redirect('/')
    
    return render_template("addnew.html")

@app.route('/sale/cars', methods=['POST'])
def create_new():
    data = {
        'price': request.form['price'],
        'description' : request.form['description'],
        'model' : request.form['model'],
        'make' : request.form['make'],
        'year' : request.form['year'],
        'users_id' : session['user_id']
    }
    if Car.validate_car(data):
        print(data)
        new_car = Car.add_car(data)
        session['car_id'] = new_car
        return redirect("/dashboard")
    return redirect('/new')

@app.route('/car/<int:car_id>')
def view_car(car_id):
    data = {
        'id': car_id
    }
    one_car =Car.get_one_user(data)
    the_car =one_car[0]
    print(the_car)
    return render_template('view.html', the_car = the_car)

@app.route('/edit/<int:car_id>')
def edit_car(car_id):
    if 'user_id' not in session:
        flash('You are not signed in. Please login.')
        return redirect('/')
    data = {
        'id': car_id,
    }
    update = Car.get_one(data)
    return render_template("edit.html",update = update)

@app.route('/edit/<int:car_id>/now', methods=['POST'])
def edit_one(car_id):
    data = {
        'id' : car_id,
        'price': request.form['price'],
        'model' : request.form['model'],
        'make' : request.form['make'],
        'year' : request.form['year'],
        'description' : request.form['description'],
        'users_id' : session['user_id']
    }
    if Car.validate_car(data):
        print(Car.validate_car(data))
        Car.edit_one(data)
        return redirect("/dashboard")
    return redirect(f'/edit/{car_id}')


@app.route("/delete/<int:car_id>")
def delete_one(car_id):
    data = {
        'id': car_id
    }
    Car.delete_one(data)
    return redirect('/dashboard')
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipes import Recipe
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
    user_ab = user_db[0]
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
    all_recipes = Recipe.get_recipes()
    print(all_recipes)
    print(session)
    return render_template('success.html', all_recipes = all_recipes)

@app.route('/logout')
def logout():
    print(session)
    session.clear()
    print(session)
    return redirect("/")

@app.route('/recipes/new')
def add_recipe():
    if 'user_id' not in session:
        flash('You are not signed in. Please login.')
        return redirect('/')
    
    return render_template("addnew.html")

@app.route('/recipes', methods=['POST'])
def create_new():
    data = {
        'name': request.form['name'],
        'description' : request.form['description'],
        'minutes' : request.form['minutes'],
        'instructions' : request.form['instructions'],
        'made_on' : request.form['made_on'],
        'users_id' : session['user_id']
    }
    if Recipe.validate_recipe(data):
        print(data)
        new_recipe = Recipe.create_recipe(data)
        session['recipe_id'] = new_recipe
        return redirect("/dashboard")
    return redirect('/recipes/new')

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    one_recipe = Recipe.get_one(data)
    return render_template('view.html', one_recipe = one_recipe)

@app.route('/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    if 'user_id' not in session:
        flash('You are not signed in. Please login.')
        return redirect('/')
    update = Recipe.get_one(data)
    return render_template("edit.html",update = update)

@app.route('/edit/now/<int:recipe_id>', methods=['POST'])
def edit_one(recipe_id):
    data = {
        'name': request.form['name'],
        'description' : request.form['description'],
        'minutes' : request.form['minutes'],
        'instructions' : request.form['instructions'],
        'made_on' : request.form['made_on'],
        'users_id' : session['user_id'],
        'id': recipe_id
    }
    if Recipe.validate_recipe(data):
        Recipe.edit_one(data)
        return redirect("/dashboard")
    return redirect('/edit/<int:recipe_id>')

@app.route("/delete/<int:recipe_id>")
def delete_one(recipe_id):
    data = {
        'id': recipe_id
    }
    Recipe.delete_one(data)
    return redirect('/dashboard')

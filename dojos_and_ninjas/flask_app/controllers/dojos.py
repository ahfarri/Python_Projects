from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja

@app.route("/dojos")
def index():
    
    dojos = Dojo.get_all()
    print(dojos)
    return render_template("index.html", all_dojos= dojos)

@app.route("/create", methods=['POST'])
def create_dojo():
    new_dojo = Dojo.create(request.form)
    print(new_dojo)
    return redirect("/dojos")

@app.route("/ninjas")
def new_ninja():
    dojos = Dojo.get_all()
    print(dojos)
    return render_template("ninjas.html", all_dojos = dojos)

@app.route("/create/new", methods=["POST"])
def create_ninja():
    data = {
        'dojo_id': request.form['dojo_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'age': request.form['age']
    }
    
    newninja = Ninja.create(data)
    print(newninja)
    return redirect(f"/dojos/{request.form['dojo_id']}")

@app.route("/dojos/<int:dojo_id>")
def show_info(dojo_id):
    data = {
        'id': dojo_id
    }
    persons = Dojo.get_all_ninjas(data)
    print(persons)
    return render_template("dojo.html", persons = persons)

# @app.route("/edit/<int:user_id>/user")
# def edit(user_id):
#     data = {
#         'id': user_id
#     }
#     person = User.get_one(data)
#     print(person)
#     return render_template("edit.html", person = person)

# @app.route("/edit/<int:user_id>", methods=["POST"])
# def edit_user(user_id):
#     data = {
#         'id': user_id,
#         'first_name': request.form['first_name'],
#         'last_name': request.form['last_name'],
#         'email': request.form['email']
#     }
    
#     User.edit_one(data)
#     return redirect(f"/show/{user_id}")

# @app.route("/delete/<int:user_id>/user")
# def delete_one(user_id):
#     data = {
#         'id': user_id
#     }
#     User.delete_one(data)
#     return redirect('/')
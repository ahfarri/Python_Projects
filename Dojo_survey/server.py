# http://localhost:5000 - have this display a nice looking HTML form.  The form should be submitted to '/process'
# Save form data into session.
# http://localhost:5000/result - have this display a html with the information that was submitted by POST

from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'life is good'

from dojo import Dojo


@app.route('/')
def index():

    return render_template("index.html")


@app.route('/process', methods=['POST'])
def process():
    if not Dojo.validate_dojo(request.form):
        return redirect('/')

    session['favorite']= request.form['language']
    session['dojo']= request.form['location']
    session['username']= request.form['name']
    session['optional']= request.form['comment']

    Dojo.save(request.form)
    print(request.form)
    return redirect('/results')

@app.route('/results')
def results():

    return render_template("results.html")

if __name__ == "__main__":
    app.run(debug=True)



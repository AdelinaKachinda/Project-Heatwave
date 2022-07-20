from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/index/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        error = None

        if not name:
            error = 'Username is required.'
        elif not location:
            error = 'Location is requred.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not confirm_password:
            error = 'Confirm-Password is required.'

        if error is None:
            # try:
            #    db.execute(
            #        "INSERT INTO user (username, password) VALUES (?, ?)",
            #        (username, generate_password_hash(password)),
            #    )
            #    db.commit()
            # except db.IntegrityError:
            #    error = f"User {username} is already registered."
            return redirect(url_for("/login"))

        # flash(error)
        # entries are invalid - reload registration page

    else:
        return render_template('/register')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

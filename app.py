from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm

app = Flask(__name__,
            static_url_path='/static')


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        location = request.form['location']

        #https://shannoncanyon-admiralwestern-5000.codio.io/#register
        #db = get_db()
        error = None

        if not name:
            error = 'Name is required.'
        elif not email:
            error = 'Email is required'
        elif not password:
            error = 'Password is required.'
        elif not confirm-password:
            error = 'Confirming the password is required.'
        elif not location:
            error = 'Location is required.'

        # if error is None:
        #     try:
        #         db.execute(
        #             "INSERT INTO user (username, password) VALUES (?, ?)",
        #             (username, generate_password_hash(password)),
        #         )
        #         db.commit()
        #     except db.IntegrityError:
        #         error = f"User {username} is already registered."
        #     else:
        #         return redirect(url_for("auth.login"))
        if error is None:
            return redirect(url_for("/index"))
        #flash(error)

    return render_template('/register')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

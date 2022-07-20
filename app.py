from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c2883c6f3a75f4135a2d0361c1ae3cb2'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.location}')"


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # checks if entries are valid
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    location=form.location.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')

        # send to login page after registering account
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

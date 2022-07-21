from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LocationForm

app = Flask(__name__,
            static_folder='../static',
            template_folder='../templates')
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


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    parent_html = "home.html"
    home_loc_form = LocationForm()

    if home_loc_form.validate_on_submit():
        pass

    return render_template('location-form.html',
                           parent_html=parent_html, loc_form=home_loc_form)


# @app.route('/location-form-home', methods=['GET', 'POST'])
# def location_form_home():
#    return render_template('location-form-home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    parent_html = "register.html"
    reg_form = RegistrationForm()
    reg_loc_form = LocationForm()

    # checks if entries are valid
    if reg_form.validate_on_submit():
        user = User(name=reg_form.name.data,
                    email=reg_form.email.data,
                    location=reg_form.location.data,
                    password=reg_form.password.data)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {reg_form.name.data}!', 'success')

        # send to login page after registering account
        return redirect(url_for('login'))

    return render_template('location-form.html', title="Register",
                           parent_html=parent_html,
                           reg_form=reg_form, loc_form=reg_loc_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

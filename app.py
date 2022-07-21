from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm
from forms import LoginForm


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
        user = User.query.filter_by(name=form.name.data).first()
        if user:
            flash("User already exist")
            return redirect(url_for('login'))
            #hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
        password = request.form.get('password')
        user = User(name=form.name.data,
                    email=form.email.data,
                    location=form.location.data,
                    password=generate_password_hash(password, method='sha256'))

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')

        # send to login page after registering account
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

# Flask_login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if user: 
            #check the password
            if check_password_hash(user.password, password):
                #login_user(user)
                flash("Log in Successful") #want this to flash with the users Name
                return redirect(url_for('home')) # if the user doesn't exist or password is wrong, reload the page
            else:
                flash("Wrong Password - Try again")

    # if the above check passes, then we know the user has the right credentials
        # email = User.query.filter_by(email=form.email.data).first()
        # if email:
        #     #not sure if this is the best way to validate password
        #     password = User.query.filter_by(password=form.password.data).first()
        #     #cursor.execute(text(<whatever_needed_to_be_casted>))
        #     #password=form.password.data
        #     #check password
        #     #if check_password_hash(user.password_hash, form.password.data)
        #     #if password:
        #     if not user or not check_password_hash(user.password, password):
        #         user = User.query.filter_by(email=email).first()
        #         # user = User.query.filter_by(name=form.name.data).first()
        #         #login_user(user) #part of flask login
        #         # flash(user)
        #         flash("Log in Successful") #want this to flash with the users Name
        #         return redirect(url_for('home'))
            # else: 
            #     flash("Wrong Password - Try again")
        else:
            flash("That user doesnt exist - Try again")
    return render_template('login.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm

app = Flask(__name__,
            static_url_path='/static')


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/index/#register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # entries are valid
    if form.validate_on_submit():
        # send form data to database
        # notify user of success

        # flash(f'Account created for {form.username.data}!', 'success')
        # send to home page
        return redirect(url_for('index'))

    # entries are invalid - reload registration page
    return render_template('/index/#register', title='Register', form=form)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


<<<<<<< HEAD
if __name__ == '__main__':      
=======
if __name__ == "__main__":
>>>>>>> 6edff745bd481705f7c2d7a5a00776139b5c6893
    app.run(debug=True, host="0.0.0.0")

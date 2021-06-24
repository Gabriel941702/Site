from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wishes.sqlite'
db = SQLAlchemy(app)


class wish(db.Model):
    nickname = db.Column(db.String(50), primary_key=True, nullable=False)
    server = db.Column(db.String(50), nullable=False)
    champion = db.Column(db.String(50), nullable=False)
    skin = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return f'nickname:{self.nickname}; server:{self.server}; champion:{self.champion}; skin:{self.skin}'


# db.create_all()


@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('user', name=username))

    return render_template('login.html')

@app.route('/<name>', methods=['POST', 'GET'])
def user(name):

    return render_template('user.html', my_name=name)


@app.route('/AboutUs')
def about_us():
    return render_template('aboutus.html')


@app.route('/download')
def download():
    return redirect('https://signup.na.leagueoflegends.com/en/signup/redownload')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return "you are logged out"

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/wish', methods=['GET', 'POST'])
def wishes():
    if request.method=='POST':
        n = request.form['nickname']
        s = request.form['server']
        c = request.form['champion']
        sk = request.form['skin']
        if n=='' or s=='' or c=='' or sk=='':
            flash('Graph is empty', 'error')
        else:
            b1 = wish(nickname=n, server=s, champion=c, skin=sk)
            db.session.add(b1)
            db.session.commit()
            flash('your wish is added', 'info')

    return render_template('wish.html')

# @app.route('/MyWishes')
# def mywishes():
#     all_wish = wish.query.all()
#     return render_template('mywishes.html',all_wish=all_wish)

if __name__ == "__main__":
    app.run(debug=True)


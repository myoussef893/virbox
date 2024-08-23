from flask import Flask, render_template,redirect,url_for,flash,session,request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_bootstrap import Bootstrap4 
from models import User,db_session,Items
from forms import LoginForm,RegisterationForm
from flask_login import LoginManager,login_required,logout_user,login_user,current_user
from random import randint
from datetime import datetime as date
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
bootstrap = Bootstrap4(app)

login_manager =LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)

@app.route('/')
def home(): 
    return render_template('./web_pages/index.html',user=current_user)

@app.route('/about')
def about():
    return render_template('404.html',user=current_user)

@app.route('/contact')
def contact():
    return "<h1> I'm the Contact Page </h1>"

@app.route('/login',methods= ["GET","POST"])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit(): 
        user = db_session.query(User).filter_by(username = form.username.data).first()
        submitted_password = form.password.data

        if user:
            password = user.password
            if check_password_hash(pwhash=password,password=submitted_password):
                login_user(user)
                print(current_user.username)

                return redirect('/dashboard')
        else: 
            error = flash('Wrong email or password.')
            return redirect('/login')

    return render_template('./web_pages/login.html',form=form,error=error,user=current_user)

@app.route('/signup',methods = ['GET','POST'])
def signup(): 
    error = None
    form = RegisterationForm()
    if form.validate_on_submit():
        u = db_session.query(User).filter_by(username = form.username.data).first()
        p = db_session.query(User).filter_by(phone = form.phone_number.data).first()
        e = db_session.query(User).filter_by(email=form.email.data).first()

        if u or p or e: 
            error = flash('User,Phone, or email already exists, please try a different one.')

        else:    
            new_user = User(
                creation_date = str(date.today().date()),
                username = form.username.data,
                full_name = form.full_name.data,
                email = form.email.data,
                phone = form.phone_number.data,
                locker = "locker-"+str(randint(10000,99999)),
                password = generate_password_hash(form.pwd.data,'pbkdf2',salt_length=8),
                group = 'Admin'
            )
            db_session.add(new_user)
            db_session.commit()
            return redirect('/login')
    
    return render_template('./web_pages/signup.html', form=form, error= error, user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/404')
def error_404():
    return render_template('404.html')

@app.route('/dashboard')
def dashboard(): 
    return render_template('./app_pages/dashboard.html',user=current_user)
    
from cart_flask import *
from items_manager import *

if __name__ == "__main__":
    app.run(debug=True)
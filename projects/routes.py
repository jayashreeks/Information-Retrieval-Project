from flask import render_template, url_for, flash, redirect
from project.models import User, Post
from project.forms import RegistrationForm, LoginForm, PostForm, SearchForm
from project import app,db
from flask_login import login_user,current_user, logout_user

@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html',title="About")

@app.route('/home')
def home():
    posts=Post.query.all()
    return render_template('home.html',posts=posts)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form=RegistrationForm()
    if form.validate_on_submit():
        #hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!You are now able to log in','success')
        return redirect(url_for('about'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and user.password==form.password.data:
            login_user(user,remember=form.remember.data)
            return redirect(url_for('about'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html',title='Login',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('about'))

@app.route('/upload/new',methods=['GET','POST'])
def upload():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(name=form.name.data,content=form.content.data,owner=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your document is uploaded','success')
        return redirect(url_for('about'))
    return render_template('upload_doc.html',title="Upload Document",form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query=form.search.data
        results = Post.query.all()
        for r in results:
            if query in r.content:
                return render_template('search_results.html',results=r)
    return render_template('search.html', title='Search',form=form)



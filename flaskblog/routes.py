from flask import render_template, url_for, request, redirect, session, flash, abort, jsonify
from flaskblog.forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm, CommentForm, CategoryForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user, logout_user, login_required
from urllib.request import urlopen
from datetime import datetime, timedelta
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post, Comment
from dataclasses import dataclass
from PIL import Image
import requests
import secrets
import json
import time
import os

db.create_all()
# Updates profile picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_name)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_name

# Saves current user information 
def catch_log():
    ip = str(request.remote_addr)
    unix_time = round(time.time())
    browser = request.user_agent.browser
    platform = request.user_agent.platform
    if ip == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + ip + '/json'
    res = urlopen(url)
    data = json.load(res)
    try:
        city = data['city']
    except:
        city = 'Unknown'

    date = datetime.utcfromtimestamp(unix_time+10800).strftime('%Y-%m-%d %H:%M:%S')
    with open("logs.txt","a") as f:
        try:
            f.write(str({"User":current_user.username, "ip":ip, "City":city, "Unix time":unix_time, "Browser":browser, "Platform":platform, "Date":date})+"\n")
        except:
            f.write(str({"User":'?', "ip":ip, "City":city, "Unix time":unix_time, "Browser":browser, "Platform":platform, "Date":date})+"\n")

@app.route("/")
@app.route("/home", methods =["GET","POST"])
def home() :
    catch_log()
    form = CategoryForm()
    if form.validate_on_submit():
        if form.category.data != 'All':
            posts = Post.query.filter_by(category=form.category.data)
        else:
            posts = Post.query.all()

        flash('Your choice has been applied!', 'success')
        return render_template('home.html', posts=posts[::-1], form=form)

    posts = Post.query.all()
    return render_template('home.html', posts=posts[::-1], form=form)

@app.route("/logs")
@login_required
def logs():
    with open("logs.txt","r") as f:
        logs = f.readlines()
    for i in range(len(logs)): logs[i] = eval(logs[i])

    return render_template('logs.html', title='Logs', logs = logs)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()

    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')   
            if next_page and next_page.count('/')>1:
                return redirect(url_for('home'))
            elif next_page:
                return redirect(url_for(f'{next_page.strip("/")}'))
            return redirect(url_for('home'))            
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')

    return render_template('login.html', error=error, title = 'Login', form=form)

@app.route("/signup", methods=['GET','POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account have been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = save_picture(form.picture.data)
            current_user.image_file = picture
        current_user.username = form.username.data
        current_user.facebook = form.facebook.data
        current_user.twitter = form.twitter.data

        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.facebook.data = current_user.facebook 
        form.twitter.data = current_user.twitter
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)

@app.route("/create_post", methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, category=form.category.data, content=form.content.data, author=current_user, author_username=current_user.username)
        db.session.add(post)
        db.session.commit()

        flash('Your post have been created!', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', title='New Post', form=form)

@app.route("/post/<int:post_id>", methods=['GET','POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = form.category.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.category.data = post.category
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post', form=form)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/post/<int:post_id>/comment", methods=['GET','POST'])
@login_required
def comment_post(post_id):

    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, commented_post=Post.query.get(post_id), commenter=current_user)
        db.session.add(comment)
        db.session.commit()

        flash('Your comment have been created!', 'success')
        
        return redirect(url_for('post', post_id=post.id))

    return render_template('comment_post.html', title='Comment Post', form=form, post=post)

#-#-# APIs #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@app.route("/api/post", methods=['GET','POST'])
def post_api():
    posts = Post.query.all()
    return jsonify({'posts':posts})

@app.route("/api/post/<int:post_id>", methods=['GET','POST'])
def post_id_api(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({'post':post})

@app.route("/api/category", methods=['GET','POST'])
def category_api():
    categories = ['General','Sports','Gaming','News','TV','Memes','Travel','Music, Art & Design']
    return jsonify({'categories':categories})

@app.route("/api/category/<string:category>", methods=['GET','POST'])
def selected_category_api(category):
    posts = Post.query.filter_by(category=category).all()
    return jsonify({'posts':posts})

@app.route("/api/user/<string:username>", methods=['GET','POST'])
def user_api(username):
    user = User.query.filter_by(username=username).first()
    posts = user.posts.all()
    return jsonify({'user':user},{'posts':posts})


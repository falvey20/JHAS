from flask import render_template, url_for, flash, redirect, request
from blog import app, db, bcrypt, mail
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddMixForm, RequestResetForm, ResetPasswordForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    searchquery = request.args.get('searchquery')
    page = request.args.get('page', 1, type=int)
    
    if searchquery:
        posts = Post.query.filter(Post.title.contains(searchquery) | Post.content.contains(searchquery)).paginate(page=page, per_page=10)
        searchtitle = searchquery
        return render_template('home.html', posts=posts, searchtitle=searchtitle)
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)

    return render_template('home.html', posts=posts)


        
        


# ABOUT
# @app.route('/about')
# def about():
#     return render_template('about.html', title='About')

# REGISTER
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, you can now Log In', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# LOGIN
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed, try again!', 'danger')
    return render_template('login.html', title='Login', form=form)

# LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# USER ACCOUNT
@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


# ADD NEW POST
@app.route('/mix/new', methods=['POST', 'GET'])
@login_required
def add_mix():
    form = AddMixForm()
    
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, content_link=form.content_link.data, theme=form.theme.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Added!', 'success')
        return redirect(url_for('home'))

    return render_template('add_mix.html', title='Add Mix/Playlist', form=form)


@app.route('/mix/<int:post_id>')
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('mix.html', title='post.title', post=post)

# DELETE POST
@app.route('/delete/<int:post_id>', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    
    db.session.delete(post)
    db.session.commit()    
    flash('Playlist deleted', 'success')
    return redirect(url_for('home'))


# RESET EMAIL
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
            sender='jhas.help@gmail.com', 
            recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: 

{url_for('reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
'''
    mail.send(msg)


# REQUEST NEW PASSWORD
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('You have been sent a password reset email', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

# RESET PASSWORD WITH TOKEN
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Reset link is invalid or has expired', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password was successfully updated, you can now Log In', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


# EDIT POST
@app.route('/editpost/<int:post_id>', methods=['POST', 'GET'])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    
    db.session.delete(post)
    db.session.commit()    
    flash('Playlist deleted', 'success')
    return redirect(url_for('home'))
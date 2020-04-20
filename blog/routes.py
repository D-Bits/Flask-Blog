from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from secrets import token_hex
from os.path import splitext, join
from flask_mail import Message
from blog.forms import RegistrationForm, LoginForm, UpdateAccountInfo, PostForm, RequestResetForm, ResetPasswordForm
from blog import app, bcrypt, db, mail
from blog.models import User, Post


@app.route("/")
@app.route("/home")
def index():

    page = request.args.get('page', 1, type=int)
    # Paginate posts, and order from most most recent to least recent
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)

    return render_template('index.html', title='Home', posts=posts)


@app.route("/about")
def about():

    image = Image.open('static/profile_pics/default.jpg')
    new_image = image.resize((400, 600))
    new_image.save('static/profile_pics/me.jpg')
        
    return render_template('about.html', title='About')


# Register new users
@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


# Logout users that are currently logged in
@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('index'))


# For saving user's profile pics
def save_picture(form_picture):

    # Generate hex code for pic
    random_hex = token_hex(8)
    _, f_ext = splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = join(app.root_path, 'static/profile_pics', picture_fn)
    # Resize image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# Route for user's account page
@app.route('/account', methods=["GET", "POST"])
@login_required
def account():

    form = UpdateAccountInfo()
    # Logic for updating user account info
    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_image_file_name = form.username.data

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account updated successfully", 'success')

        return redirect(url_for('account'))

    # Populate form fields w/ users's current info
    elif request.method == "GET":

        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.profile_image_file_name)

    return render_template('account.html', title="My Account", image_file=image_file, form=form)


# Route for creating new posts
@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():

    form = PostForm()

    if form.validate_on_submit():

        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")


# Route for using individual posts
@app.route('/post/<int:post_id>')
def individual_post(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title=post.title, post=post)
    

# Route for individual user's posts
@app.route("/user/<string:username>")
def user_posts(username):

    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # Paginate posts, and order from most most recent to least recent
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)

    return render_template('user_posts.html', title='Home', user=user, posts=posts)


# Update existing posts
@app.route('/post/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def update_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm() 

    if form.validate_on_submit():
        # Ensure fields are already populated w/ current post data
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        
        flash("Your post has been updated", 'success')
        return redirect(url_for('individual_post', post_id=post.id))

    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post', form=form, legend="Update Post")


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')

    return redirect(url_for('index'))


# To be used in reset_request() route
def send_reset_email(user):

    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@example.com', recipients=[user.email])

    msg.body = f"""
To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request, simple ignore this email.
    """
    # Send the message
    mail.send(msg)


# Request password reset route
@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():

    # Don't allow reset if user is logged in
    if current_user.is_authenticated:

        return redirect(url_for('home'))

    form = RequestResetForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Reset email with instructions sent. Please check your inbox.', 'info')
        return redirect(url_for('login'))
    
    return render_template('reset_request.html', title='Reset Password', form=form)


# Route for template to actually reset password
@app.route("/reset_password", methods=["GET", "POST"])
def reset_token(token):

    # Don't allow reset if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token()
    if not user:
        flash("Invalid or expired token", "warning")
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password == hashed_pass
        db.session.commit()
        flash('Your password has been updated. You are now able to log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_token.html', title='Reset Password', form=form)

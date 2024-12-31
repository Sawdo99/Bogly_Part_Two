"""Blogly application."""

from flask import Flask
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def root():
    """Homepage redirects to list of users"""

    return redirect("/users")

@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404

# User Route --------------------------------------------------------------------------

#List all users
@app.route('/users')
def users_index():
    
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template(users/index.html, users=users)

# Show details
@app.route('/users', method=["GET"])
def users_details():
    return render_template("details.html")


# Add new user
@app.route('/users', methods=["GET"])
def new_user_form():
    return render_template('new.html')

#Process added user
@app.route('/users/new', methods=['POST'])
def add_user():
    new_id = max(users.keys()) + 1 if users else 1
    name = request.form['name']
    users[new_id] = {"name": name}
    return redirect('/users')
#show user
@app.route('/users/<int:user_id>')
def users_show(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

#Edit user
@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

#process edited user
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

#Processing deleting user
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# Post Routes ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# show's form for new post 
@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

# form submission
@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

# shows specific post
@app.route('/posts/<int:post_id>')
def posts_show(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

# show post
@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

# edit post
@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")

# delete post
@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")
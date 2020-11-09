import datetime
import hashlib
import uuid

from flask import Flask, render_template, request, make_response, redirect, url_for

from model import db, User, Post, Comment

app = Flask(__name__)

db.create_all()

WEBSITE_LOGIN_COOKIE_NAME = "science/session_token"
COOKIE_DURATION = 900  # in seconds


def require_session_token(func):
    """Decorator to require authentication to access routes"""

    def wrapper(*args, **kwargs):
        session_token = request.cookies.get(WEBSITE_LOGIN_COOKIE_NAME)
        redirect_url = request.path or '/'

        if not session_token:
            app.logger.error('no token in request')
            return redirect(url_for('login', redirectTo=redirect_url))

        user = db.query(User) \
            .filter_by(session_cookie=session_token) \
            .filter(User.session_expiry_datetime >= datetime.datetime.now()) \
            .first()

        if not user:
            app.logger.error(f'token {session_token} not valid')
            return redirect(url_for('login', redirectTo=redirect_url))

        app.logger.info(
            f'authenticated user {user.username} with token {user.session_cookie} valid until {user.session_expiry_datetime.isoformat()}')
        request.user = user
        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper


def provide_user(func):
    """Decorator to read user info if available"""

    def wrapper(*args, **kwargs):
        session_token = request.cookies.get(WEBSITE_LOGIN_COOKIE_NAME)

        if not session_token:
            request.user = None
            return func(*args, **kwargs)

        user = db.query(User)\
            .filter_by(session_cookie=session_token)\
            .filter(User.session_expiry_datetime >= datetime.datetime.now())\
            .first()

        request.user = user
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper



@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        repeat = request.form.get("repeat")

        if password != repeat:
            return "Password and Repeat do not match! Please try again."

        # query, check if there is a user with this username in the DB
        # user = db.query(User).filter(User.username == username).one()  # -> needs to find one, otherwise raises Error
        # user = db.query(User).filter(User.username == username).first()  # -> find first entry, if no entry, return None
        # users = db.query(User).filter(User.username == username).all()  # -> find all, always returns list. if not entry found, empty list

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # # right way to find user with correct password
        # user = db.query(User)\
        #     .filter(User.username == username, User.password_hash == password_hash)\
        #     .first()

        user = db.query(User).filter(User.username==username).first()

        session_cookie = str(uuid.uuid4())
        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=COOKIE_DURATION)

        if user is None:
            user = User(username=username,
                        password_hash=password_hash,
                        session_cookie=session_cookie,
                        session_expiry_datetime=expiry_time)
            db.add(user)
            db.commit()
            app.logger.info(f"User {username} is registered.")

        elif user.password_hash != password_hash:
            app.logger.info(f"User {username} failed to login with wrong password.")
            redirect_url = request.args.get('redirectTo')
            return redirect(url_for('login', redirectTo=redirect_url))

        else:
            user.session_cookie = session_cookie
            user.session_expiry_datetime = expiry_time
            db.add(user)
            db.commit()
            app.logger.info(f"User {username} is logged in")

        redirect_url = request.args.get('redirectTo')
        response = make_response(redirect(redirect_url))
        response.set_cookie(WEBSITE_LOGIN_COOKIE_NAME, session_cookie, httponly=True, samesite='Strict')
        return response

    elif request.method == "GET":
        cookie = request.cookies.get(WEBSITE_LOGIN_COOKIE_NAME)
        user = None

        if cookie is not None:
            user = db.query(User) \
                .filter_by(session_cookie=cookie) \
                .filter(User.session_expiry_datetime >= datetime.datetime.now())\
                .first()

        if user is None:
            logged_in = False
        else:
            logged_in = True

        return render_template("login.html", logged_in=logged_in)

# TODO homework until nov 12th:
# '/registration'
#

@app.route('/about', methods=["GET"])
@provide_user
def about():
    return render_template("about.html")


@app.route('/faq', methods=["GET"])
@require_session_token
def faq():
    return render_template("faq.html")


@app.route('/logout', methods=["GET"])
@provide_user
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie(WEBSITE_LOGIN_COOKIE_NAME, expires=0)

    user = db.query(User)\
        .filter_by(username=request.user.username)\
        .first()

    if user is not None:
        # reset user
        user.session_expiry_datetime = None
        user.session_cookie = None
        db.add(user)
        db.commit()
        app.logger.info(f"{user.username} has logged out.")

    return response


@app.route('/blog', methods=["GET", "POST"])
@require_session_token
def blog():

    current_user = request.user

    if request.method == "POST":
        title = request.form.get("posttitle")
        text = request.form.get("posttext")
        post = Post(
            title=title, text=text,
            user=current_user
        )
        db.add(post)
        db.commit()
        return redirect(url_for('blog'))

    if request.method == "GET":
        posts = db.query(Post).all()
        return render_template("blog.html", posts=posts)


@app.route('/posts/<post_id>', methods=["GET", "POST"])
@require_session_token
def posts(post_id):
    current_user = request.user
    post = db.query(Post).filter(Post.id == post_id).first()

    if request.method == "POST":
        text = request.form.get("text")
        comment = Comment(
            text=text,
            post=post,
            user=current_user
        )
        db.add(comment)
        db.commit()
        return redirect('/posts/{}'.format(post_id))

    elif request.method == "GET":
        comments = db.query(Comment).filter(Comment.post_id == post_id).all()
        return render_template('posts.html', post=post, comments=comments)


if __name__ == '__main__':
    app.run(host='localhost', port=7890)

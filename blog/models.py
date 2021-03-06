from blog import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Profile pic
    profile_image_file_name = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # One-to-Many relationship to Post
    posts = db.relationship('Post', backref="author", lazy=True)

    # Define how objects are printed out
    def __repr__(self):

        return f"User('{self.username}', '{self.email}', '{self.profile_image_file_name}')"

    # Create password reset token that expires in 30 min
    def get_reset_token(self, expires_seconds=1800):

        s = Serializer(app.config['SECRET_KEY'], expires_seconds)

        return s.dumps({"user_id": self.id}).decode('utf-8')

    # Verify reset token
    @staticmethod
    def verify_reset_token(token):

        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    
    # Define how objects are printed out
    def __repr__(self):

        return f"Post('{self.title}', '{self.date_posted}')"
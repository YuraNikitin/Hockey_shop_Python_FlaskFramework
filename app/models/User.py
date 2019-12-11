from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from flask_login import current_user
from app.models.Cart import CartItems


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', lazy='joined')

    def __repr__(self):
        return '<User:{}, surname: {}, name: {}, address:{}, email: {}'.format(self.username, self.surname, self.name,
                                                                               self.address, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def count_products_inCart(self):
        return CartItems.query.filter_by(user_id=current_user.id).count()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<  name: {}, id:{}'.format( self.name, self.id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
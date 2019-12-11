from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

dirname = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(dirname, 'static/images/')
app = Flask(__name__, static_url_path='/static/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(Config)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app.routes import cart,product,user
from app.models import Cart,Product,User

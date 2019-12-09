from app import app, db
from app.models import User, Product, CartItems, CategoryProduct,Role


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Product': Product, 'CartItems': CartItems, 'CategoryProduct': CategoryProduct,'Role':Role }

from app import app, db
from app.models.User import User, Role
from app.models.Cart import CartItems
from app.models.Product import Product, CategoryProduct

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Product': Product, 'CartItems': CartItems, 'CategoryProduct': CategoryProduct,
            'Role': Role}

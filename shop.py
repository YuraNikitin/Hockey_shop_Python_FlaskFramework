from app import app, db
from app.models.cart import CartItems
from app.models.product import Product, CategoryProduct
from app.models.user import User, Role


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 'User': User, 'Product': Product, 'CartItems': CartItems,
        'CategoryProduct': CategoryProduct, 'Role': Role
    }

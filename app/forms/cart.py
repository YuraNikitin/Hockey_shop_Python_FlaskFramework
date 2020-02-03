from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CartForm(FlaskForm):
    """This form to add position product, contains following fields:"""
    product_id = StringField('Product id')
    count_prod = StringField('Укажите кол-во: ', validators=[DataRequired()])
    submit = SubmitField('Add')


class CartItemForm(FlaskForm):
    """This form to delete a position product, contains following fields:"""
    item_id = StringField('Product id')
    submit = SubmitField('Delete')


class CartItemFormDeleteAll(FlaskForm):
    """This form to delete all products in cart, contains following fields:"""
    submit = SubmitField('Delete All')

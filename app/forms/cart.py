from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CartForm(FlaskForm):
    product_id = StringField('Product id')
    count_prod = StringField('Укажите кол-во: ', validators=[DataRequired()])
    submit = SubmitField('Add')


class CartItemForm(FlaskForm):
    item_id = StringField('Product id')
    submit = SubmitField('Delete')


class CartItemFormDeleteAll(FlaskForm):
    submit = SubmitField('Delete All')
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class AddProduct(FlaskForm):
    name = StringField('Name Product', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField("Категория", coerce=int)
    submit = SubmitField('ADD')


class DeleteProduct(FlaskForm):
    product_id = StringField('Product id')
    submit = SubmitField('Delete')

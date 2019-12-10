from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Entry')


class EditProfileForm(FlaskForm):
    username = StringField('New username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Change')


class RegistrationForm(EditProfileForm, FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This e-mail is busy. Please use a different e-mail!')


class CartForm(FlaskForm):
    product_id = StringField('Product id')
    count_prod = StringField('Укажите кол-во: ', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddProduct(FlaskForm):
    name = StringField('Name Product', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField("Категория", coerce=int)
    submit = SubmitField('ADD')


class CartItemForm(FlaskForm):
    item_id = StringField('Product id')
    submit = SubmitField('Delete')


class CartItemFormDeleteAll(FlaskForm):
    submit = SubmitField('Delete All')


class DeleteProduct(FlaskForm):
    product_id = StringField('Product id')
    submit = SubmitField('Delete')

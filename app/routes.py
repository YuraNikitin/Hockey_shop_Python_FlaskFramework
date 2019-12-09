from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
import os
from app import app
from app.forms import LoginForm, RegistrationForm, EditProfileForm, CartForm, AddProduct, CartItemForm, \
    CartItemFormDeleteAll, DeleteProduct
from flask_login import current_user, login_user, logout_user
from app.models import User, Product, CartItems, CategoryProduct, Role
from app import db


@app.route('/', defaults={'category_id': None})
@app.route('/index/<int:category_id>', methods=['GET', 'POST'])
def index(category_id):
    page = request.args.get('page', 1, type=int)
    if category_id is not None:
        products = Product.query.filter_by(category_id=category_id).paginate(page, app.config['PRODUCT_PER_PAGE'],
                                                                             False)
        next_url = url_for('index', category_id=category_id, page=products.next_num) if products.has_next else None
        prev_url = url_for('index', category_id=category_id, page=products.prev_num) if products.has_prev else None
    else:
        products = Product.query.paginate(page, app.config['PRODUCT_PER_PAGE'], False)
        next_url = url_for('index', page=products.next_num) if products.has_next else None
        prev_url = url_for('index', page=products.prev_num) if products.has_prev else None
    return render_template('index.html', title='Home page', items=products.items,
                           category=CategoryProduct.query.all(), next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("SORRY Invalid password or username")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, name=form.name.data, surname=form.surname.data,
                    email=form.email.data, address=form.address.data, role_id=2)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("GREAT your are now registered user!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/product/<id>')
def product(id):
    form = CartForm()
    del_prod=DeleteProduct()
    product = Product.query.filter_by(id=id).first_or_404()
    return render_template('product.html', product=product, form=form, del_prod=del_prod)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        db.session.commit()
        flash("Great your changes are saved!")
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.email.data = current_user.email
        form.address.data = current_user.address

    return render_template('edit_profile.html', title='Edit profile', form=form)


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    form = CartForm()
    cart_item_form = CartItemForm()
    cart_item_delete_all = CartItemFormDeleteAll()
    if form.validate_on_submit():
        cartitems = CartItems(user_id=current_user.id, product_id=form.product_id.data, count=form.count_prod.data)
        db.session.add(cartitems)
        db.session.commit()
        flash('You add product in cart')
        return redirect(url_for('index'))
    else:
        item = CartItems.query.filter_by(user_id=current_user.id).all()
        price_product = {}
        for i in item:
            price_product[i.id] = i.product.price * i.count
        total_sum = sum(price_product.values())
        return render_template('cart.html', title='Cart', item=item, total_sum=total_sum, price_product=price_product,
                               form=form, cart_item_form=cart_item_form, cart_item_delete_all=cart_item_delete_all)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProduct()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        category = CategoryProduct.query.filter_by(id=form.category.data).first()
        product = Product(name=form.name.data, price=int(form.price.data), description=form.description.data,
                          image=filename, category_id=int(category.id))
        db.session.add(product)
        db.session.commit()
        flash(filename)
        return redirect(url_for('index'))
    else:
        form.category.choices = [(c.id, c.category_name) for c in CategoryProduct.query.order_by('id')]
    return render_template('add_product.html', title='ADD', form=form)


@app.route('/edit_product/<id>', methods=['GET', 'POST'])
def edit_product(id):
    form = AddProduct()
    product = Product.query.filter_by(id=id).first_or_404()
    form.category.choices = [(c.id, c.category_name) for c in CategoryProduct.query.order_by('id')]
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        product.category_id = form.category.data
        product.image = filename
        db.session.commit()
        flash("Great your changes are saved!")
        return redirect(url_for('index', username=current_user.username))
    elif request.method == 'GET':
        form.name.data = product.name
        form.price.data = product.price
        form.description.data = product.description
        form.category.data = product.category_id
    return render_template('edit_product.html', title='Edit profile', form=form, product=product)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = CartItemFormDeleteAll()
    if form.validate_on_submit():
        db.session.query(CartItems).filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('You  product delete in cart')
        return redirect(url_for('cart'))
    return render_template('cart.html')


@app.route('/delete_position', methods=['GET', 'POST'])
def delete_position():
    cart_item_form = CartItemForm()
    if cart_item_form.validate_on_submit():
        db.session.query(CartItems).filter_by(id=cart_item_form.item_id.data).delete()
        db.session.commit()
        flash('You  product delete in cart')
        return redirect(url_for('cart'))
    return render_template('cart.html')


@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product():
    del_prod = DeleteProduct()
    if del_prod.validate_on_submit():
        db.session.query(Product).filter_by(id=del_prod.product_id.data).delete()
        db.session.commit()
        flash('You  product delete')
        return redirect(url_for('index'))
    return render_template('index.html')


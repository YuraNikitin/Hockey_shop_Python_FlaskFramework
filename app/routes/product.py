from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
import os
from app import app
from app.forms.cart import CartForm
from app.forms.Product import DeleteProduct, AddProduct
from flask_login import current_user
from app.models.Product import Product, CategoryProduct
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


@app.route('/product/<id>')
def product(id):
    form = CartForm()
    del_prod = DeleteProduct()
    product = Product.query.filter_by(id=id).first_or_404()
    return render_template('Product/product.html', product=product, form=form, del_prod=del_prod)


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
    return render_template('Product/add_product.html', title='ADD', form=form)


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
    return render_template('Product/edit_product.html', title='Edit profile', form=form, product=product)


@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product():
    del_prod = DeleteProduct()
    if del_prod.validate_on_submit():
        db.session.query(Product).filter_by(id=del_prod.product_id.data).delete()
        db.session.commit()
        flash('You  product delete')
        return redirect(url_for('index'))
    return render_template('index.html')

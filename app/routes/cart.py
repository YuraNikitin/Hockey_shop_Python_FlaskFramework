from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from app import app
from app import db
from app.forms.cart import CartForm, CartItemForm, CartItemFormDeleteAll
from app.models.cart import CartItems


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    form = CartForm()
    cart_item_form = CartItemForm()
    cart_item_delete_all = CartItemFormDeleteAll()

    if form.validate_on_submit():
        cart_items = CartItems(user_id=current_user.id, product_id=form.product_id.data, count=form.count_prod.data)
        db.session.add(cart_items)
        db.session.commit()
        flash('You add product in cart')
        return redirect(url_for('index'))
    else:
        item = CartItems.query.filter_by(user_id=current_user.id).all()
        price_product = {}
        for i in item:
            price_product[i.id] = i.product.price * i.count
        total_sum = sum(price_product.values())

        return render_template(
            'Cart/cart.html', title='Cart', item=item, total_sum=total_sum, price_product=price_product,
            form=form, cart_item_form=cart_item_form, cart_item_delete_all=cart_item_delete_all
        )


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = CartItemFormDeleteAll()

    if form.validate_on_submit():
        db.session.query(CartItems).filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('You  product delete All in cart')
        return redirect(url_for('cart'))
    return render_template('Cart/cart.html')


@app.route('/delete_position', methods=['GET', 'POST'])
def delete_position():
    cart_item_form = CartItemForm()

    if cart_item_form.validate_on_submit():
        db.session.query(CartItems).filter_by(id=cart_item_form.item_id.data).delete()
        db.session.commit()
        flash('You  product delete in cart')
        return redirect(url_for('cart'))

    return render_template('Cart/cart.html')

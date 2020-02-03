from app import db


class CartItems(db.Model):
    """This model Cart, contains following fields:"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    count = db.Column(db.Integer)
    product = db.relationship('Product', lazy='joined')

    def __repr__(self):
        return '< Product item {} , user_id {}, prod_id {}>'.format(self.id, self.user_id, self.product_id)

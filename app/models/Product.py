from app import db


class CategoryProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(128))

    def __repr__(self):
        return '< CategoryProduct item {} >'.format(self.id)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    description = db.Column(db.String(128))
    image = db.Column(db.String(128))
    category_id = db.Column(db.Integer, db.ForeignKey('category_product.id'))
    category = db.relationship('CategoryProduct', lazy='joined')

    def __repr__(self):
        return '< Product {} >'.format(self.name)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    serialize_rules = ('-reviews.customer',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    #relationship mapping review to cutomer
    reviews = db.relationship('Review', back_populates='customer')  
    
    #association proxy to get list of items through customer's reviews relationship
    items = association_proxy('reviews', 'item', creator=(lambda item_obj: Review(item=item_obj))) 
    

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    
    serialize_rules = ('-reviews.item',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    
    #relationship mapping  review to item
    reviews = db.relationship('Review', back_populates='item', lazy='joined')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
    
class Review(db.Model, SerializerMixin):
    """Review model for items."""

    __tablename__ = 'reviews'
    
    serialize_rules = ('-customer.reviews', '-item.reviews',)

    # fields that are common to all reviews (i.e., not specific to a particular item review or customer review)
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    # Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    
    customer = db.relationship('Customer', back_populates='reviews')  # one review is written by one customer
    item = db.relationship('Item', back_populates='reviews')   # a review can be related to an item or not at all


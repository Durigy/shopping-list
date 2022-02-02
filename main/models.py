from datetime import datetime
from email.policy import default
import secrets
from main import db, login_manager
from flask_login import UserMixin


#############################
#                           #
#       User Stuff          #
#                           #
#############################

class User(UserMixin, db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key=True, default=secrets.token_hex(10)) # Must be randomly generated
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # Links (ForeignKeys)
    # Add here

    # Relationships
    shopping_list = db.relationship('ShoppingList', backref='user', lazy=True, foreign_keys = 'ShoppingList.user_id')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#############################
#                           #
#       List Stuff          #
#                           #
#############################

class ShoppingList(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key=True, default=secrets.token_hex(10)) # Must be randomly generated
    name = db.Column(db.String(128), unique=False, nullable=False)
    item_count = db.Column(db.Integer, nullable=False, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Links (ForeignKeys)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)

    # Relationships 
    shopping_list_item = db.relationship('ShoppingListItem', backref='shopping_list', lazy=True, foreign_keys = 'ShoppingListItem.shopping_list_id')

class ShoppingListItem(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key=True, default=secrets.token_hex(10)) # Must be randomly generated
    name = db.Column(db.String(128), unique=False, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    in_trolley = db.Column(db.Boolean, nullable=False, default=False)
    # priority = db.Column(db.Integer, nullable=False, default=1)

    # Links (ForeignKeys)
    shopping_list_id = db.Column(db.String(20), db.ForeignKey('shopping_list.id'), nullable=False)

    # Relationships
    # Add here

from flask_login import UserMixin

from sqlalchemy.orm import relationship

import json

from apps import db, login_manager, bcrypt

import uuid

from datetime import datetime

class Users(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username      = db.Column(db.String(64), unique=True, nullable=False)
    email         = db.Column(db.String(128), unique=True, nullable=False)
    password      = db.Column(db.String(128), nullable=False)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    update_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)
    suspended = db.Column(db.Boolean, default=False)
    extend_existing=True

    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)


    def __repr__(self):
        return str(self.username)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

class RoadData(db.Model):
    __table_args__ = {'extend_existing': True}

    __tablename__ = 'road_data'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    province = db.Column(db.String(64))
    city = db.Column(db.String(100))
    street_name = db.Column(db.String(200))
    video_path = db.Column(db.String(254))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    update_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    children = db.relationship('RoadDamage', backref='parent', cascade='all, delete-orphan')


class RoadDamage(db.Model):
    __table_args__ = {'extend_existing': True}

    __tablename__ = 'road_damage'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sum_damage = db.Column(db.Integer, nullable=False)
    type_damage = db.Column(db.String(100), nullable=False)
    road_data_id = db.Column(db.String(36), db.ForeignKey("road_data.id", ondelete="cascade"), nullable=False)


import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    lvl_click = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

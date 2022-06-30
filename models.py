import datetime as _dt
from email.policy import default
from operator import index
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database

# class Book(_database.Base):
#     __tablename__ = 'book'
    
#     id = _sql.Column(_sql.Integer, primary_key=True)
#     title = _sql.Column(_sql.String)
#     description = _sql.Column(_sql.String)

class User(_database.Base):
    __tablename__ ="users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String)
    hashed_password = _sql.Column(_sql.String)
    leads = _orm.relation("Lead", back_populates="owner")
    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)
    
class Lead(_database.Base):
    __tablename__ = "leads"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    first_name = _sql.Column(_sql.String, index=True)
    last_name = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, index=True)
    company = _sql.Column(_sql.String, index=True, default="")
    note = _sql.Column(_sql.String, default="")
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    owner = _orm.relationship("User", back_populates="leads")
#!/usr/bin/env python
# encoding: utf-8
from app import db
from datetime import datetime
from enum import Enum
import json

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d")]

class Status(Enum):
    archived = 0
    active = 1
    suspended = 2     
    def __repr__(self):
        return [{row.value:row.name} for row in self]
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100), index=True, nullable=False)
    registry_id = db.Column(db.Integer, index=True, \
        nullable=False, unique=True)
    status = db.Column(db.Integer, default=1)
    address = db.Column(db.String(200))
    established = db.Column(db.Date, index=True, nullable=False)
    total_capital = db.Column(db.Float)
    company_owners = db.relationship("NpOwnerAssociation", 
        backref="company_np_owners", lazy='dynamic')
    company_jp_owners = db.relationship("JpOwnerAssociation", 
        backref="company_jp_owners", lazy='dynamic')
    def __repr__(self):
        return json.dumps(self.serialize)    
    @property
    def serialize(self):
       return {
           'id'             : self.id,
           'name'           : self.name,
           'registry_id'    : self.registry_id,
           'established'     : dump_datetime(self.established)
       } 
    # TODO: add_owner(), remove_owner(), archive_company()
    # TODO: create_jp_person()
class Individual(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_dttm = db.Column(db.DateTime, 
        server_default=db.func.current_timestamp())
    first_name = db.Column(db.String(100), index=True, nullable=False)
    last_name = db.Column(db.String(100), index=True)
    identificator = db.Column(db.BIGINT, unique=True)
    email = db.Column(db.String(120))
    status = db.Column(db.Integer, default=1)   
    companies_owned = db.relationship("NpOwnerAssociation", 
        backref="companies_owned", lazy='dynamic') 
    
    def __repr__(self):
        return json.dumps(self.serialize)    
    @property
    def serialize(self):
       return {
            'id':self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'identificator':self.identificator
       }   
    # TODO: get_companies(), archive_individual()
class JPInvididual(db.Model):
    __tablename__ = 'juridicial_persons'
    id = db.Column(db.Integer, primary_key=True)
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100), index=True, nullable=False)
    registry_id = db.Column(db.Integer, index=True, \
        nullable=False, unique=True)
    status = db.Column(db.Integer, default=1)
    companies_owned = db.relationship("JpOwnerAssociation", 
        backref="companies_owned", lazy='dynamic')    
    def __repr__(self):
        return json.dumps(self.serialize)    
    @property
    def serialize(self):
       return {
           'id'             : self.id,
           'name'           : self.name,
           'registry_id'    : self.registry_id,
       }
    
    # TODO: get_companies(), archive_jpindividual()
class NpOwnerAssociation(db.Model):
    __tablename__ = 'np_owner_association'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('individual.id'), 
        primary_key=True)
    owned_id = db.Column(db.Integer, db.ForeignKey('company.id'), 
        primary_key=True)
    shares = db.Column(db.Float)
    dttm = db.Column(db.DateTime, default=datetime.utcnow)
    founder = db.Column(db.Boolean)
    np_owner_a = db.relationship("Individual", backref="companies_np_owned")
    company = db.relationship("Company", backref="np_owners")
class JpOwnerAssociation(db.Model):
    __tablename__ = 'jp_owner_association'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('juridicial_persons.id'), 
        primary_key=True)
    owned_id = db.Column(db.Integer, db.ForeignKey('company.id'), 
        primary_key=True)
    shares = db.Column(db.Float)
    dttm = db.Column(db.DateTime, default=datetime.utcnow)
    founder = db.Column(db.Boolean)
    jp_owner_a = db.relationship("JPInvididual", backref="companies_jp_owned")
    company = db.relationship("Company", backref="jp_owners") 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect
from flask import url_for, request, make_response
from app import app
from werkzeug.urls import url_parse
import sys, os
from app.models import Status, Company, Individual, JPInvididual
from app.models import NpOwnerAssociation, JpOwnerAssociation
from app.forms import AddCompanyForm

from flask import jsonify
from flask import json
from app import db
import math

from sqlalchemy import or_
from datetime import datetime, date, timedelta

import config
from config import logger


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    try:
        logger.info("""\n===========================\n
            routes.py:index:method{0}\n{1}"""
            .format(request.method, request.args))
        
        companies = Company.query \
            .filter(Company.status != Status.archived.value).all()
        return render_template('index.html', pages=None, data=companies)
    except Exception as e:
        logger.error("""\n===========================\n
            routes.py:index:ERROR\n{0}""".format(e))

@app.route('/search', methods=['GET'])
def search_company():
    """
    - osaühingu nime ja/või registrikoodi järgi ning osaniku nime ja/või koodi järgi
    - fragmendi järgi otsing
    searches companies based on registry_id, name, owner name or owner code
    """
    try:
        logger.info("""\n===========================\n
            routes.py:search_company:method{0}\n{1}"""
            .format(request.method, request.args))
        search_key = request.args.get('search_string', '')
        if search_key:        
            found_items = Company.query\
                .filter(Company.status != Status.archived.value)\
                .filter(or_(Company.name.ilike('%{0}%'.format(search_key)),
                Company.registry_id.ilike('%{0}%'.format(search_key)))).all()   
            return jsonify(repr(found_items))
        return redirect(url_for('index'))
    except Exception as e:
        logger.error("""\n===========================\n
            routes.py:search_company:ERROR\n{0}""".format(e))
@app.route('/search_persons', methods=['GET'])
def search_persons():
    """
    searches persons either natural or juridicial based on registry_id, name
    """
    try:
        logger.info("""\n===========================\n
            routes.py:search_company:method{0}\n{1}"""
            .format(request.method, request.args))
        search_key = request.args.get('search_string', '')
        if search_key:        
            found_jp = Company.query\
                .filter(Company.status != Status.archived.value)\
                .filter(or_(Company.name.ilike('%{0}%'.format(search_key)),
                Company.registry_id.ilike('%{0}%'.format(search_key)))).all() 
            found_np = Individual.query\
                .filter(Individual.status != Status.archived.value).filter(\
                or_(Individual.first_name.ilike('%{0}%'.format(search_key)),
                Individual.identificator.ilike('%{0}%'.format(search_key)),
                Individual.last_name.ilike('%{0}%'.format(search_key)))).all() 
            data = {
                'juridicial_persons': repr(found_jp),
                'natural_persons':repr(found_np)}
            return jsonify(data)
        else:
            return '', 200
    except Exception as e:
        logger.error("""\n===========================\n
            routes.py:search_company:ERROR\n{0}""".format(e))           
def apply_company_values(company):
    """
    format input values per Company model
    """
    try:
        registry_id=company['identificator']
        exists = Company.query \
            .filter(Company.registry_id == registry_id).first() 
        print(exists, registry_id)        
        if not exists and company['identificator']!= 0 and \
            company['company_name'] != "" and len(company['company_name'])>=3\
            and len(company['company_name'])<=100 and int(registry_id)>=1 and\
            int(registry_id)<=9999999:
            datetime_object = datetime \
                .strptime(company['established_date'], '%Y.%m.%d')
            cmpny_to_add = Company(
                name=company['company_name'],   
                registry_id=company['identificator'], 
                total_capital=company['total_capital'],            
                established=datetime_object)
            return cmpny_to_add
        return exists
    except Exception as e:
        logger.info("""\n===========================\n
            routes.py:apply_company_values:method\n{}"""
            .format(e))
 
def apply_natural_person_values(person):
    """
    format input values per Individual model
    """
    try:
        registry_id = person['natural_person_registry_id']
        exists = Individual.query.filter \
            (Individual.identificator == registry_id).first()
        if not exists and int(registry_id)<=69999999999 and \
        int(registry_id)>=30001010000 and \
        person['natural_person_first_name']!="":                
            person_to_add = Individual(
                first_name=person['natural_person_first_name'],   
                last_name=person['natural_person_last_name'], 
                identificator=registry_id)            
            return person_to_add
        return exists   
    except Exception as e:
        logger.info("""\n===========================\n
            routes.py:apply_natural_person_values:method\n{}"""
            .format(e))
def apply_jp_values(company):
    try:        
        jp_person = JPInvididual(
                name=company.name,   
                registry_id=company.registry_id)
        print(jp_person)
        return jp_person
    except Exception as e:
        logger.info("""\n===========================\n
            routes.py:apply_natural_person_values:method\n{}"""
            .format(e))
@app.route('/add', methods=['POST'])
def add_company():
    try:
        companies = request.get_json() 
        logger.info("""\n===========================\n
            routes.py:add_company:method{0}\n{1}"""
            .format(request.method, companies))           
        print(json.dumps(companies, sort_keys=True, indent=3))
        for company in companies:
            cmpny_to_add = apply_company_values(company)
            if cmpny_to_add:                
                db.session.add(cmpny_to_add)
                db.session.add(apply_jp_values(cmpny_to_add))
            for item in company['shareholders_natural_persons']:  
                person=company['shareholders_natural_persons'][item]
                person_to_add = apply_natural_person_values \
                    (person)  
                if person_to_add: 
                    db.session.add(person_to_add)                    
                    a = NpOwnerAssociation(shares=person['shares'],
                        founder=True, owner_id=person_to_add.id)
                    a.companies_np_owned = person_to_add
                    cmpny_to_add.company_owners.append(a)
                    db.session.commit()
            for item in company['shareholders_juridical_persons']:  
                registry_id=item['identificator']
                jp_person=company['shareholders_juridical_persons'][item]
                jp_to_add = Company.query \
                    .filter(Company.registry_id == registry_id).first()
                if jp_to_add: 
                    print(jp_to_add)
                    db.session.add(jp_to_add)
                    a = JpOwnerAssociation(shares=jp_person['shares'],
                        founder=True, owner_id=jp_to_add.id)
                    a.companies_np_owned = jp_to_add
                    cmpny_to_add.company_owners.append(a)
                    db.session.commit()
        return redirect(url_for('index'))
    except Exception:
        logger.error("""\n===========================\n
            routes.py:add_company:ERROR\n""".format())
@app.route('/new_company', methods=['GET','POST'])
def new_company():
    try:
        logger.info("""\n===========================\n
            routes.py:new_company:method{0}"""
            .format(request.method,))
        form = AddCompanyForm()
        return render_template('new_company.html', form=form)
            
    except Exception as e:
        logger.error("""\n===========================\n
            routes.py:new_company:ERROR\n{0}""".format(e))
def company_form(form, company, np_owners=None, jp_owners=None):
    form.company_name.data=company.name
    form.identificator.data=company.registry_id   
    form.total_capital.data=company.total_capital
    form.established_date.data=company.established
    np_owner_list = []
    for np_owner in np_owners:
        owner_dict = {}
        owner_dict["natural_person_first_name"]=np_owner['owner'].first_name
        owner_dict["natural_person_last_name"]=np_owner['owner'].last_name
        owner_dict["natural_person_registry_id"]=np_owner['owner'].identificator
        owner_dict["shares"]=np_owner['shares']
        owner_dict["founder"]=np_owner['founder']
        np_owner_list.append(owner_dict)
    form.np_owners = np_owner_list   
    return form    
def get_np_owners(company):
    np_owners = []
    for assoc in company.company_owners:
        out={}
        out['founder'] = assoc.founder
        out['shares'] = assoc.shares
        out['owner'] = assoc.np_owner_a
        np_owners.append(out)
    return np_owners
def get_jp_owners(company):
    jp_owners = []
    for assoc in company.company_jp_owners:
        out={}
        print(assoc)
        out['founder'] = assoc.founder
        out['shares'] = assoc.shares
        out['owner'] = assoc.jp_owner_a
        jp_owners.append(out)
    return jp_owners
@app.route('/get_data/<int:company_id>', methods=['GET'])
def get_data(company_id):
    logger.info("""\n===========================\n
        routes.py:get_data:method{0}"""
        .format(request.method))
    company_data = Company.query.get(company_id)
    np_owners = get_np_owners(company_data)
    jp_owners = get_jp_owners(company_data)
    print(np_owners, jp_owners)
    form = company_form(AddCompanyForm(), company_data, \
        np_owners=np_owners, jp_owners=jp_owners)    
    #try:
    return render_template('company_view.html', form=form)
    """except Exception as e:
        logger.error(""""""\n===========================\n
            routes.py:get_data:ERROR\n{0}"""""".format(e))"""

#!/usr/bin/env python
# encoding: utf-8
"""
Adds some companie to database.
Makes inquiry to database to get shareholders and adds randomly to companies
"""
import random, os
import pymysql
import sys, json
from enum import Enum 

from datetime import date, datetime
from config import logger
from config import Config as config
from app import db
from app.models import Status, Company, Individual, JPInvididual
from app.models import NpOwnerAssociation, JpOwnerAssociation
from app.routes import apply_jp_values
def generate_dataset(names): 
    """
    Generates dataset for testing purposes
    """
    dataset = []
    ids = random.sample(range(1, 9999999), len(names))    
    for i, company in enumerate(names):
        year = random.randint(1950, 2018)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        established_date = datetime(year, month, day)
        cmpny_to_add = {
            'name'           : company.strip(),
            'registry_id'    : ids[i],
            'established'    : established_date}
        dataset.append(cmpny_to_add)
    return dataset    

def add_company(dataset):
    companies = []
    individuals = list(Individual.query.all())
    for i, cmpy in enumerate(dataset):
        jpindividuals = list(JPInvididual.query.all())
        total_capital = 0
        cmpny_to_add = Company(
            name=cmpy['name'],   
            registry_id=cmpy['registry_id'],  
            established=cmpy['established']
            )
        if len(dataset)<11:
            qty = len(dataset)
        else:
            qty = 10
        shareholders = random.sample(individuals, random.randint(1,qty))
        if len(jpindividuals)<5:
            qty = len(jpindividuals)
        else:
            qty = 5
        if jpindividuals:
            jp_shareholders = random.sample(jpindividuals,
                random.randint(1,qty))
            for owner in jp_shareholders:
                print(owner)
                shares = random.randint(2500,5000)
                total_capital += shares
                a = JpOwnerAssociation(shares=shares, 
                    founder=bool(random.getrandbits(1)), 
                    owner_id=owner.id)
                a.companies_jp_owned = owner
                cmpny_to_add.company_jp_owners.append(a)
        for owner in shareholders:
            print(owner)
            shares = random.uniform(2500,5000)
            total_capital += shares
            a = NpOwnerAssociation(shares=shares, 
                founder=bool(random.getrandbits(1)), 
                owner_id=owner.id)
            a.companies_np_owned = owner
            cmpny_to_add.company_owners.append(a)
        
        cmpny_to_add.total_capital = total_capital
        print(cmpny_to_add)
        db.session.add(cmpny_to_add)
        db.session.add(apply_jp_values(cmpny_to_add))
        new_entries = db.session.commit()
    
    return new_entries
  
if __name__=="__main__":
    try:
        dataset = []
        
        with open("F:\\git\\osayhing\\shareholders.txt",'r') as f:
            test_companies = random.sample([name for name in f],100)  
            dataset = generate_dataset(test_companies)
            print(add_company(dataset))    
    except Exception as e:
        print("Exception occured\n{0}".format(e,))


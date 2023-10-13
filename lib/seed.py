#!/usr/bin/env python3

from random import choice as rc
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from models import Company, Dev, Freebie

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

swag = ['t-shirt', 'hat', 'water bottle', 'pen', 'sticker', 
        'keychain', 'notebook', 'mouse pad', 'yoga mat', 'frisbee', 
        'chapstick', 'lanyard', 'tote bag', 'reusable straw set', 
        'hoodie', 'koozie', 'mug', 'tumbler', 'beanie', 'socks', 
        'sunglasses', 'umbrella', 'yo-yo', 'calendar', 'duffle bag']

def create_companies():
    companies = [
        Company(
            name = fake.company(),
            founding_year = fake.year()
        ) 
    for i in range(20)]
    session.add_all(companies)
    session.commit()
    return companies

def create_devs():
    devs = [
        Dev(
            name = fake.name()
        ) 
    for i in range(100)]
    session.add_all(devs)
    session.commit()
    return devs

def create_freebies():
    freebies = [
        Freebie(
            item_name = random.choice(swag),
            value = random.randint(0, 100)
        ) 
    for i in range(300)]
    session.add_all(freebies)
    session.commit()
    return freebies

def delete_records():
    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()

def relate_companies_to_devs(companies, devs):
    for company in companies:
        for i in range(random.randint(1, 10)):
            dev = random.choice(devs)
            if company not in dev.companies:
                dev.companies.append(company)
                session.add(dev)
                session.commit()
    return companies, devs

def relate_freebies(companies, devs, freebies):
    for freebie in freebies:
        freebie.company = rc(companies)
        freebie.dev = rc(devs)
        
    session.add_all(freebies)
    session.commit()
    return companies, devs, freebies

if __name__ == '__main__':
    delete_records()
    companies = create_companies()
    devs = create_devs()
    freebies = create_freebies()
    companies, devs = relate_companies_to_devs(companies, devs)
    companies, devs, freebies = relate_freebies(companies, devs, freebies)

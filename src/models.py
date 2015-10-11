# John Eargle
# 2015

import sys

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()



class Place(Base):
    """
    Physical location.
    """
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    country = Column(String)
    state = Column(String)
    county = Column(String)
    city = Column(String)
    street = Column(String)
    street_id = Column(String)   # street number
    unit = Column(String)        # unit/apt number
    postal_code = Column(String)
    latitude = Column(Numeric)
    longitude = Column(Numeric)

    def __repr__(self):
        return "<Place(country='%s', state='%s', street_id='%s', street='%s')>" % (
            self.country, self.state, self.street_id, self.street)


class Organization(Base):
    """
    Community of people.  Business, non profit, club, forum, etc.
    """
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    webpage = Column(Integer, ForeignKey('webpages.id'))
    user_webpage = Column(Integer, ForeignKey('webpages.id'))
    address = Column(Integer, ForeignKey('places.id'))

    def __repr__(self):
        return "<Organization(name='%s', url='%s', user_url='%s')>" % (
            self.name, self.webpage.url, self.user_webpage.url)


class Person(Base):
    """
    Human in the world.
    """
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    sex = Column(String)
    address = Column(Integer, ForeignKey('places.id'))

    def __repr__(self):
        return "<Person(name='%s', fullname='%s')>" % (
            self.name, self.fullname)


class Webpage(Base):
    """
    Identity associated with an online community.
    """
    __tablename__ = 'webpages'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)

    def __repr__(self):
        return "<Webpage(name='%s', url='%s')>" % (
            self.name, self.url)


class Account(Base):
    """
    Identity associated with an online community.
    """
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    person = Column(Integer, ForeignKey('people.id'))
    organization = Column(Integer, ForeignKey('organizations.id'))
    webpage = Column(Integer, ForeignKey('webpages.id'))

    def __repr__(self):
        return "<Account(name='%s', url='%s')>" % (
            self.name, self.webpage.url)



if __name__=='__main__':
    pass

# John Eargle
# 2015

import sys

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship



Base = declarative_base()


class Place(Base):
    """
    Physical location.
    """
    __tablename__ = 'place'

    place_id = Column(Integer, primary_key=True)
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

    org_places = relationship('OrganizationPlace')
    organizations = association_proxy(
        'org_places',
        'organization')

    person_places = relationship('PersonPlace')
    people = association_proxy(
        'person_places',
        'person')
        
    def __repr__(self):
        return "<Place(country='%s', state='%s', street_id='%s', street='%s')>" % (
            self.country, self.state, self.street_id, self.street)


class Organization(Base):
    """
    Community of people.  Business, non profit, club, forum, etc.
    """
    __tablename__ = 'organization'

    org_id = Column(Integer, primary_key=True)
    name = Column(String)
    webpage = Column(Integer, ForeignKey('webpage.webpage_id'))
    user_webpage = Column(Integer, ForeignKey('webpage.webpage_id'))

    org_places = relationship('OrganizationPlace')
    addresses = association_proxy('org_places', 'place')
    
    def __repr__(self):
        return "<Organization(name='%s', url='%s', user_url='%s')>" % (
            self.name, self.webpage.url, self.user_webpage.url)


class Person(Base):
    """
    Human in the world.
    """
    __tablename__ = 'person'

    person_id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    sex = Column(String)

    person_places = relationship('PersonPlace')
    addresses = association_proxy('person_places', 'place')

    def __repr__(self):
        return "<Person(name='%s', fullname='%s')>" % (
            self.name, self.fullname)


class Webpage(Base):
    """
    Identity associated with an online community.
    """
    __tablename__ = 'webpage'

    webpage_id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)

    def __repr__(self):
        return "<Webpage(name='%s', url='%s')>" % (
            self.name, self.url)


class Account(Base):
    """
    Identity associated with an online community.
    """
    __tablename__ = 'account'

    account_id = Column(Integer, primary_key=True)
    name = Column(String)
    person = Column(Integer, ForeignKey('person.person_id'))
    organization = Column(Integer, ForeignKey('organization.org_id'))
    webpage = Column(Integer, ForeignKey('webpage.webpage_id'))

    def __repr__(self):
        return "<Account(name='%s', url='%s')>" % (
            self.name, self.webpage.url)


class OrganizationPlace(Base):
    """
    Association table for Organizations and Places with many-to-many semantics.
    """
    __tablename__ = 'organization_place'
    
    org_id = Column(Integer, ForeignKey('organization.org_id'), primary_key=True)
    place_id = Column(Integer, ForeignKey('place.place_id'), primary_key=True)


class PersonPlace(Base):
    """
    Association table for People and Places with many-to-many semantics.
    """

    __tablename__ = 'person_place'

    person_id = Column(Integer, ForeignKey(Person.person_id),
                             primary_key=True)
    place_id = Column(Integer, ForeignKey(Place.place_id),
                      primary_key=True)


class PersonPerson(Base):
    """
    Association table for People with other People with many-to-many semantics.
    """

    __tablename__ = 'person_person'

    parent_id = Column(Integer, ForeignKey(Person.person_id),
                       primary_key=True)
    child_id = Column(Integer, ForeignKey(Person.person_id),
                      primary_key=True)
    label = Column(String)
    


if __name__=='__main__':
    pass

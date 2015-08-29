# John Eargle
# 2015

import sys

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db', echo=True)
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
    url = Column(String)
    user_url = Column(String)
    address = Column(Integer, ForeignKey('places.id'))

    def __repr__(self):
        return "<Organization(name='%s', url='%s', user_url='%s')>" % (
            self.name, self.url, self.user_url)


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


class Account(Base):
    """
    Identity associated with an online community.
    """
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    person = Column(Integer, ForeignKey('people.id'))
    organization = Column(Integer, ForeignKey('organizations.id'))
    name = Column(String)

    def __repr__(self):
        return "<User(name='%s', url='%s')>" % (
            self.name, self.url)


Base.metadata.create_all(engine)



if __name__=='__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    reddit_address = Place(country='USA', state='CA',
                           city='San Francisco', street='3rd Street',
                           street_id='520', postal_code='94107')
    session.add(reddit_address)
    session.commit()
    
    reddit = Organization(name='reddit',
                          url='http://www.reddit.com',
                          user_url='http://www.reddit.com/u',
                          address=reddit_address.id)
    session.add(reddit)
    freenode = Organization(name='freenode',
                            url='irc://irc.freenode.org')
    session.add(freenode)
    john = Person(name='John', fullname='John Doe', sex='m')
    session.add(john)
    dummy1 = Person(name='dummy1')
    session.add(dummy1)
    session.commit()

    dummy_reddit = Account(organization=reddit.id, person=dummy1.id, name='dummy')
    session.add(dummy_reddit)
    dummy_irc = Account(organization=freenode.id, person=dummy1.id, name='dummy')
    session.add(dummy_irc)

    session.commit()
    

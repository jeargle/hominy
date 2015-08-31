# John Eargle
# 2015

import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.models import Base, Place, Organization, Person, Account

engine = create_engine('sqlite:///test.db', echo=True)
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
    
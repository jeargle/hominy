# John Eargle
# 2015

import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.models import Base, Place, Organization, Person, Webpage, Account

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

    reddit_main = Webpage(name='reddit',
                          url='http://www.reddit.com',
    )
    reddit_user = Webpage(name='reddit_user',
                          url='http://www.reddit.com/u',
    )
    reddit = Organization(name='reddit',
                          webpage=reddit_main.id,
                          user_webpage=reddit_user.id,
                          address=reddit_address.id)
    session.add(reddit_main)
    session.add(reddit_user)
    session.add(reddit)

    freenode_main = Webpage(name='freenode',
                            url='irc://irc.freenode.org')
    freenode = Organization(name='freenode',
                            webpage=freenode_main.id)
    session.add(freenode_main)
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
    

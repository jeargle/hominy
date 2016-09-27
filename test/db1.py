# John Eargle
# 2015

import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from hominy.main.models import Base, Place, Organization
from hominy.main.models import Person, Webpage, Account, DataFile

engine = create_engine('sqlite:///test.db', echo=True)
Base.metadata.create_all(engine)


def make_reddit(session):
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
                          webpage=reddit_main.webpage_id,
                          user_webpage=reddit_user.webpage_id,
                          # addresses=[reddit_address.place_id],
    )

    session.add(reddit_main)
    session.add(reddit_user)
    session.add(reddit)

    return reddit


def make_freenode(session):
    freenode_main = Webpage(name='freenode',
                            url='irc://irc.freenode.org')
    freenode = Organization(name='freenode',
                            webpage=freenode_main.webpage_id)
    session.add(freenode_main)
    session.add(freenode)

    return freenode


if __name__=='__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    reddit = make_reddit(session)
    freenode = make_freenode(session)

    john = Person(name='John', fullname='John Doe', sex='m')
    session.add(john)

    dummy1 = Person(name='dummy1')
    session.add(dummy1)
    session.commit()

    dummy_reddit = Account(organization_id=reddit.org_id, person_id=dummy1.person_id, name='dummy')
    session.add(dummy_reddit)
    dummy_irc = Account(organization_id=freenode.org_id, person_id=dummy1.person_id, name='dummy')
    session.add(dummy_irc)
    
    session.commit()
    

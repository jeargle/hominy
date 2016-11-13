# John Eargle
# 2015-2016

import os.path
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from hominy.datafile.models import DataFile
from hominy.main.models import Base, Element, Note
from hominy.person.models import Person
from hominy.place.models import Place
from hominy.organization.models import Organization
from hominy.webpage.models import Webpage, Account

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


def make_datafile(session):
    path1 = os.path.realpath(__file__)
    df1 = DataFile(name=os.path.basename(path1),
                   path=os.path.dirname(path1))
    session.add(df1)

    return df1



if __name__=='__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    freenode = make_freenode(session)
    df1 = make_datafile(session)
    reddit = make_reddit(session)
    reddit.add_note('Reddit note 1')
    reddit.add_note('Reddit note 2')
    df1.add_element(reddit)

    note1 = Note(note='Hey, this is my note!', element=df1)
    session.add(note1)
    note2 = Note(note='Hey, this is my second note!', element=df1)
    session.add(note2)

    john = Person(name='John', fullname='John Doe', sex='m')
    session.add(john)

    dummy1 = Person(name='dummy1')
    session.add(dummy1)
    session.commit()

    dummy_reddit = Account(organization_id=reddit.org_id,
                           person_id=dummy1.person_id,
                           name='dummy')
    session.add(dummy_reddit)
    dummy_irc = Account(organization_id=freenode.org_id,
                        person_id=dummy1.person_id,
                        name='dummy')
    session.add(dummy_irc)
    
    session.commit()
    

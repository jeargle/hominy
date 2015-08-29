# John Eargle
# 2015

import sys

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()



class Organization(Base):
    """
    Community of people.  Business, non profit, club, forum, etc.
    """
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    user_url = Column(String)

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

    reddit = Organization(name='reddit',
                          url='http://www.reddit.com',
                          user_url='http://www.reddit.com/u/')
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
    

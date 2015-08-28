# John Eargle
# 2015

import sys

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


class Organization():
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    

    
class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<Person(name='%s', fullname='%s')>" % (
            self.name, self.fullname)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    person = Column(Integer, ForeignKey('people.id'),
                    primary_key=True)
    name = Column(String)
    url = Column(String)

    def __repr__(self):
        return "<User(name='%s', url='%s')>" % (
            self.name, self.url)


Base.metadata.create_all(engine)


if __name__=='__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    

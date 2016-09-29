# John Eargle
# 2015-2016

from datetime import datetime
import os.path
import sys
import uuid

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy import DateTime, Boolean, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from guid import GUID

from hominy.main.models import CLS_INDEX, CLS_NAMES
from hominy.main.models import Element, Base


class Organization(Element):
    """
    Community of people.  Business, non profit, club, forum, etc.
    """
    __tablename__ = 'organization'

    org_id = Column(Integer,
                    ForeignKey(Element.element_id),
                    primary_key=True)
    webpage = Column(Integer, ForeignKey('webpage.webpage_id'))
    user_webpage = Column(Integer, ForeignKey('webpage.webpage_id'))

    org_places = relationship('OrganizationPlace')
    addresses = association_proxy('org_places', 'place')
    
    __mapper_args__ = {
        'polymorphic_identity': CLS_INDEX['Organization'],
        'with_polymorphic': '*',
        'inherit_condition': (org_id == Element.element_id)
    }
    
    def __repr__(self):
        return "<Organization(name='%s', url='%s', user_url='%s')>" % (
            self.name, self.webpage.url, self.user_webpage.url)

    def as_dict(self):
        d = Element.as_dict(self)

        return d

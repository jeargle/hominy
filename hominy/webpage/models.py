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
from sqlalchemy.orm import relationship

from guid import GUID

from hominy.main.models import CLS_INDEX, CLS_NAMES
from hominy.main.models import Element, Base



class Webpage(Element):
    """
    Identity associated with an online community.
    """
    __tablename__ = 'webpage'

    webpage_id = Column(Integer,
                       ForeignKey(Element.element_id),
                       primary_key=True)
    # name = Column(String)
    webpage_url = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': CLS_INDEX['Webpage'],
        'with_polymorphic': '*',
        'inherit_condition': (webpage_id == Element.element_id)
    }

    def __repr__(self):
        return "<Webpage(name='%s', url='%s')>" % (
            self.name, self.url)

    def as_dict(self):
        d = Element.as_dict(self)

        d['webpage_url'] = self.webpage_url

        return d
    

class Account(Element):
    """
    Identity associated with an online community.
    """
    __tablename__ = 'account'

    account_id = Column(Integer,
                        ForeignKey(Element.element_id),
                        primary_key=True)
    # name = Column(String)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    organization_id = Column(Integer, ForeignKey('organization.org_id'))
    webpage_id = Column(Integer, ForeignKey('webpage.webpage_id'))

    __mapper_args__ = {
        'polymorphic_identity': CLS_INDEX['Account'],
        'with_polymorphic': '*',
        'inherit_condition': (account_id == Element.element_id)
    }

    def __repr__(self):
        return "<Account(name='%s', url='%s')>" % (
            self.name, self.webpage.url)

    def as_dict(self):
        d = Element.as_dict(self)

        return d


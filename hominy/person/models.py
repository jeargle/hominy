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
from hominy.place.models import Place


class Person(Element):
    """
    Human in the world.
    """
    __tablename__ = 'person'

    person_id = Column(Integer,
                       ForeignKey(Element.element_id),
                       primary_key=True)
    # name = Column(String)
    fullname = Column(String)
    sex = Column(String)

    person_places = relationship('PersonPlace')
    addresses = association_proxy('person_places', 'place')

    __mapper_args__ = {
        'polymorphic_identity': CLS_INDEX['Person'],
        'with_polymorphic': '*',
        'inherit_condition': (person_id == Element.element_id)
    }

    def __repr__(self):
        return "<Person(name='%s', fullname='%s')>" % (
            self.name, self.fullname)

    def as_dict(self):
        d = Element.as_dict(self)

        d['fullname'] = self.fullname
        d['sex'] = self.sex

        return d


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


class PersonPlace(Base):
    """
    Association table for People and Places with many-to-many semantics.
    """

    __tablename__ = 'person_place'

    person_id = Column(Integer, ForeignKey(Person.person_id),
                             primary_key=True)
    place_id = Column(Integer, ForeignKey(Place.place_id),
                      primary_key=True)

# John Eargle
# 2015

from datetime import datetime
import sys
import uuid

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy import DateTime, Boolean, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from guid import GUID


Base = declarative_base()


CLS_INDEX = {
        # "Abstract base classes"
        'Element'              : 0,
        # 1xx for Place related elements
        'Place'                : 100,
        # 2xx for Organization releated elements
        'Organization'         : 200,
        # 3xx for Person related elements
        'Person'               : 300,
        # 4xx for Webpage related elements
        'Webpage'              : 400,
        # 5xx for Account related elements
        'Account'              : 500,
}

# Backwards mapping so it's easy to get the string version of class id
CLS_NAMES = dict((v, k) for k, v in CLS_INDEX.items())

# Basic sanity check
if len(CLS_INDEX) != len(CLS_NAMES):
    raise Exception("CLS_INDEX is not a unique mapping!")




class Element(Base):
    """
    """

    __tablename__ = 'element'

    element_id = Column(Integer, primary_key=True)
    uuid = Column(GUID, unique=True)
    name = Column(String)
    url = Column(String)   # URL that points to the element
    desc = Column(String)
    element_class = Column(Integer, default=CLS_INDEX['Element'])

    # TODO: find way to make create_timestamp WORM (write-once, read-many)
    created_timestamp = Column(DateTime, nullable=False)
    updated_timestamp = Column(DateTime, nullable=False)

    __mapper_args__ = {
        'polymorphic_on': element_class,
        'polymorphic_identity': CLS_INDEX['Element']
    }

    def __init__(self, *args, **kwargs):
        e_uuid = kwargs.get('uuid', None)
        if e_uuid is None:
            kwargs['uuid'] = str(uuid.uuid4())
        elif not is_valid_uuid(e_uuid):
            raise ValueError('bad UUID: "%s"' % e_uuid)

        # SQLAlchemy __init__
        Base.__init__(self, *args, **kwargs)

        self.created_timestamp = datetime.utcnow()
        self.updated_timestamp = self.created_timestamp

        return
    
    @property
    def class_name(self):
        return CLS_NAMES[self.element_class]

    def as_dict(self, deep_copy=False, params=None):
        return {
            'uuid'   : str(self.uuid),
            'url'    : self.url,
            'element_class'    : self.class_name,
            'name'   : self.name,
            'desc'   : self.desc,
            'created_at': self.created_timestamp.isoformat() + 'Z',
            'updated_at': self.updated_timestamp.isoformat() + 'Z' if self.updated_timestamp else None,
            'meta'   : self.meta,
            #'priors' : [(prior.uuid, prior.label) for prior in self.priors]
        }

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'@%{}'.format(self.name)


class Place(Element):
    """
    Physical location.
    """
    __tablename__ = 'place'

    place_id = Column(Integer,
                      ForeignKey(Element.element_id),
                      primary_key=True)
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

    org_places = relationship('OrganizationPlace')
    organizations = association_proxy(
        'org_places',
        'organization')

    person_places = relationship('PersonPlace')
    people = association_proxy(
        'person_places',
        'person')

    __mapper_args__ = {
        'polymorphic_identity': CLS_INDEX['Place'],
        'with_polymorphic': '*',
        'inherit_condition': (place_id == Element.element_id)
    }
    
    def __repr__(self):
        return "<Place(country='%s', state='%s', street_id='%s', street='%s')>" % (
            self.country, self.state, self.street_id, self.street)


class Organization(Element):
    """
    Community of people.  Business, non profit, club, forum, etc.
    """
    __tablename__ = 'organization'

    org_id = Column(Integer,
                    ForeignKey(Element.element_id),
                    primary_key=True)
    # name = Column(String)
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


class OrganizationPlace(Base):
    """
    Association table for Organizations and Places with many-to-many semantics.
    """
    __tablename__ = 'organization_place'
    
    org_id = Column(Integer, ForeignKey('organization.org_id'), primary_key=True)
    place_id = Column(Integer, ForeignKey('place.place_id'), primary_key=True)


class PersonPlace(Base):
    """
    Association table for People and Places with many-to-many semantics.
    """

    __tablename__ = 'person_place'

    person_id = Column(Integer, ForeignKey(Person.person_id),
                             primary_key=True)
    place_id = Column(Integer, ForeignKey(Place.place_id),
                      primary_key=True)


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
    


if __name__=='__main__':
    pass
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

    def as_dict(self):
        d = Element.as_dict(self)

        d['country'] = self.country
        d['state'] = self.state
        d['county'] = self.county
        d['city'] = self.city
        d['street'] = self.street
        d['street_id'] = self.street_id
        d['unit'] = self.unit
        d['postal_code'] = self.postal_code
        d['latitude'] = self.latitude
        d['longitude'] = self.longitude
        
        return d

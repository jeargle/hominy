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
        # 6xx for DataFile related elements
        'DataFile'             : 600,
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

    notes = relationship('Note', back_populates='element')

    datafile_elements = relationship(
            'DataFileElement', back_populates='element',
            foreign_keys='DataFileElement.element_id',
    )
    datafiles = association_proxy('datafile_elements', 'datafile')


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

    def add_note(self, note_string):
        note = Note(note=note_string, element=self)
        self.notes.append(note)

    def add_datafile(self, df):
        self.datafiles.append(df)
    
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'@%{}'.format(self.name)



class Note(Base):
    """
    String which can be associated with an arbitrary Element.
    """
    __tablename__ = 'note'

    note_id = Column(Integer,
                     primary_key=True)
    note = Column(String)

    element_id = Column(Integer, ForeignKey(Element.element_id))
    element = relationship('Element', back_populates='notes')

    def __repr__(self):
        return "<Note(name='%s')>" % (self.name)

    def as_dict(self):
        d = {}
        d['note'] = self.note

        return d

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



class DataFile(Element):
    """
    Data file which can be assoicated with an arbitrary Element.
    """
    __tablename__ = 'datafile'

    datafile_id = Column(Integer,
                         ForeignKey(Element.element_id),
                         primary_key=True)
    # path on local filesystem, not including final '/'
    # "os.path.join(self.path, self.name)" is the full path
    path = Column(String)

    datafile_elements = relationship('DataFileElement')
    elements = association_proxy('datafile_element', 'element')

    __mapper_args__ = {
        'polymorphic_identity': CLS_INDEX['DataFile'],
        'with_polymorphic': '*',
        'inherit_condition': (datafile_id == Element.element_id)
    }

    @property
    def fullpath(self):
        return os.join(self.path, self.name)
    
    def __repr__(self):
        return "<DataFile(name='%s')>" % (self.name)

    def as_dict(self):
        d = Element.as_dict(self)

        d['path'] = self.path

        return d    


class DataFileElement(Base):
    """
    Association table for DataFiles and Elements with many-to-many semantics.
    """

    __tablename__ = 'datafile_element'

    datafile_id = Column(Integer, ForeignKey(DataFile.datafile_id),
                         primary_key=True)
    element_id = Column(Integer, ForeignKey(Element.element_id),
                        primary_key=True)

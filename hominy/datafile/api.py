# John Eargle
# 2015-2016

# CRUD functions for hominy models

from hominy.datafile.models import DataFile
from hominy.main.api import __apply_filters
from hominy.main.models import CLS_INDEX, CLS_NAMES
from hominy.main.models import Base, Element



#
# DataFile
#

def create_datafile(session=None, **values):
    time = datetime.utcnow()

    datafile = DataFile(created_timestamp=timestamp, **values)
    session.add(datafile)
    session.flush()

    return datafile.as_dict()


def request_datafile(filters=None, session=None):
    filters = filters or {}

    # DataFile
    q = session.query(DataFile)
    q = __apply_filters(q, DataFile, session, **filters)

    a_dicts = [a.as_dict() for a in q.all()]

    return a_dicts


def update_datafile():
    pass


def delete_datafile():
    pass


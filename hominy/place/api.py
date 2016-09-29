# John Eargle
# 2015-2016

# CRUD functions for hominy models

from hominy.main.api import __apply_filters
from hominy.main.models import CLS_INDEX, CLS_NAMES
from hominy.place.models import Place



#
# Place
#

def create_place(session=None, **values):
    time = datetime.utcnow()

    place = Place(created_timestamp=timestamp, **values)
    session.add(place)
    session.flush()

    return place.as_dict()


def request_place(filters=None, session=None):
    filters = filters or {}

    # Place
    q = session.query(Place)
    q = __apply_filters(q, Place, session, **filters)

    p_dicts = [p.as_dict() for p in q.all()]

    return p_dicts

def update_place():
    pass

def delete_place():
    pass


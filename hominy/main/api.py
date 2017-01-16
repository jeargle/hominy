# John Eargle
# 2015-2016

# CRUD functions for hominy models

from hominy.main.models import Base, Element

# from hominy.datafile.models import DataFile
from hominy.organization.models import Organization
from hominy.person.models import Person
from hominy.place.models import Place
from hominy.webpage.models import Webpage, Account


def __apply_element_filters(query, session=None, **filters):

    target_filters = [
        'uuid', 'name', 'url', 'desc', 'element_class',
    ]

    for tf in target_filters:
        if tf in filters:
            query = query.filter(Element.getattr(tf) == filters[tf])
            filters.pop(tf)

    return query


def __apply_filters(query, target, session=None, **filters):

    target_filters = []
    if target == Place:
        target_filters = [
            'country', 'state', 'county', 'city', 'street',
            'street_id', 'unit', 'postal_code', 'latitude',
            'longitude',
        ]
    elif target == Organization:
        target_filters = [
            'webpage', 'user_webpage',
        ]
    elif target == Person:
        target_filters = [
            'fullname', 'sex',
        ]
    elif target == Webpage:
        target_filters = [
            'webpage_url',
        ]
    elif target == Account:
        target_filters = [
            'person', 'organization', 'webpage',
        ]
    
    for tf in target_filters:
        if tf in filters:
            query = query.filter(target.getattr(tf) == filters[tf])
            filters.pop(tf)

    query = __apply_element_filters(query, session, filters)
    return query


#
# Note
#

def create_note(session=None, **values):
    time = datetime.utcnow()

    note = Note(created_timestamp=timestamp, **values)
    session.add(note)
    session.flush()

    return note.as_dict()


def request_note(uuid, session=None):
    filters = {'uuid': uuid}

    # Note
    q = session.query(Note)
    q = __apply_filters(q, Note, session, **filters)

    note_dict = q.first().as_dict()

    return note_dict


def request_notes(filters=None, session=None):
    filters = filters or {}

    # Note
    q = session.query(Note)
    q = __apply_filters(q, Note, session, **filters)

    note_dicts = [n.as_dict() for n in q.all()]

    return note_dicts


def update_note():
    pass


def delete_note():
    pass


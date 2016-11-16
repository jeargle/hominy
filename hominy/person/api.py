# John Eargle
# 2015-2016

# CRUD functions for hominy models

from hominy.main.api import __apply_filters
from hominy.main.models import CLS_INDEX, CLS_NAMES
from hominy.person.models import Person



#
# Person
#

def create_person(session=None, **values):
    time = datetime.utcnow()

    person = Person(created_timestamp=timestamp, **values)
    session.add(person)
    session.flush()

    return person.as_dict()


def request_person(filters=None, session=None):
    filters = {'uuid': uuid}

    # Person
    q = session.query(Person)
    q = __apply_filters(q, Person, session, **filters)

    person_dict = q.first().as_dict()

    return person_dict


def request_people(filters=None, session=None):
    filters = filters or {}

    # Person
    q = session.query(Person)
    q = __apply_filters(q, Person, session, **filters)

    person_dicts = [p.as_dict() for p in q.all()]

    return person_dicts


def update_person():
    pass


def delete_person():
    pass


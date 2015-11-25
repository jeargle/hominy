# John Eargle
# 2015

# CRUD functions for hominy models

from hominy.main.models import Base, Element, Place, Organization, Person, Webpage, Account


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


#
# Organization
#

def create_organization(session=None, **values):
    time = datetime.utcnow()

    org = Organization(created_timestamp=timestamp, **values)
    session.add(org)
    session.flush()

    return org.as_dict()


def request_organization(filters=None, session=None):
    filters = filters or {}

    # Organization
    q = session.query(Organization)
    q = __apply_filters(q, Organization, session, **filters)

    o_dicts = [o.as_dict() for o in q.all()]

    return o_dicts


def update_organization():
    pass


def delete_organization():
    pass


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
    filters = filters or {}

    # Person
    q = session.query(Person)
    q = __apply_filters(q, Person, session, **filters)

    p_dicts = [p.as_dict() for p in q.all()]

    return p_dicts


def update_person():
    pass


def delete_person():
    pass


#
# Webpage
#

def create_webpage(session=None, **values):
    time = datetime.utcnow()

    webpage = Webpage(created_timestamp=timestamp, **values)
    session.add(webpage)
    session.flush()

    return webpage.as_dict()


def request_webpage(filters=None, session=None):
    filters = filters or {}

    # Webpage
    q = session.query(Webpage)
    q = __apply_filters(q, Webpage, session, **filters)

    w_dicts = [w.as_dict() for w in q.all()]

    return w_dicts


def update_webpage():
    pass


def delete_webpage():
    pass


#
# Account
#

def create_account(session=None, **values):
    time = datetime.utcnow()

    account = Account(created_timestamp=timestamp, **values)
    session.add(account)
    session.flush()

    return account.as_dict()


def request_account(filters=None, session=None):
    filters = filters or {}

    # Account
    q = session.query(Account)
    q = __apply_filters(q, Account, session, **filters)

    a_dicts = [a.as_dict() for a in q.all()]

    return a_dicts


def update_account():
    pass


def delete_account():
    pass


# John Eargle
# 2015

# CRUD functions for hominy models

from src.main.models import Base, Place, Organization, Person, Webpage, Account


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
        ]
    elif target == Person:
        target_filters = [
        ]
    elif target == Webpage:
        target_filters = [
        ]
    elif target == Account:
        target_filters = [
        ]
    
    for tf in target_filters:
        if tf in filters:
            query = query.filter(target.getattr(tf) == filters[tf])
            filters.pop(tf)

    return query


#
# Place
#

def create_place():
    pass

def request_place(filters=None, session=None, agent=None):
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

def create_organization():
    pass

def request_organization(filters=None, session=None, agent=None):
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

def create_person():
    pass

def request_person(filters=None, session=None, agent=None):
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

def create_webpage():
    pass

def request_webpage(filters=None, session=None, agent=None):
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

def create_account():
    pass

def request_account(filters=None, session=None, agent=None):
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


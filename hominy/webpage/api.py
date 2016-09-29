# John Eargle
# 2015-2016

# CRUD functions for hominy models

from hominy.main.api import __apply_filters
from hominy.main.models import CLS_INDEX, CLS_NAMES
from hominy.webpage.models import Webpage


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


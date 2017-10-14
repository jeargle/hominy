# John Eargle
# 2015-2016

# CRUD functions for hominy models


from hominy.organization.models import Organization
from hominy.main.api import __apply_filters
from hominy.main.models import CLS_INDEX, CLS_NAMES
from hominy.main.models import Base, Element


#
# Organization
#

def create_organization(session=None, **values):
    time = datetime.utcnow()

    org = Organization(created_timestamp=timestamp, **values)
    session.add(org)
    session.flush()

    return org.as_dict()


def request_organizations(filters=None, session=None):
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

"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth, T
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

OLIVE_KINDS = {'k': 'Kalamata', 'l': 'Ligurian'}

db.define_table(
    'olives',
    Field('olive_name'),
    Field('olive_kind'),
    Field('weight_tot', 'double'),
    Field('weight_net', 'double'),
)

# This should not appear in forms.
db.olives.id.readable = db.olives.id.writable = False

db.olives.olive_name.label = T("Name")
db.olives.olive_name.requires = IS_LENGTH(minsize=2)

db.olives.olive_kind.requires = IS_IN_SET(OLIVE_KINDS)
db.olives.olive_kind.default = 'k'

db.olives.weight_tot.label = "Weight (gross)"
db.olives.weight_tot.requires=IS_FLOAT_IN_RANGE(
        0, 1000, error_message=T("Please enter a weigh in grams between 0 and 1Kg"))

db.olives.weight_net.label = "Weight (net, dry)"
db.olives.weight_net.requires=IS_FLOAT_IN_RANGE(
        0, 1000, error_message=T("Please enter a weigh in grams between 0 and 1Kg"))

db.commit()

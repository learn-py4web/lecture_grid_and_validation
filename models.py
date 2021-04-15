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

db.define_table(
    'olives',
    Field('olive_name'),
    Field('olive_kind'),
    Field('weight_tot', 'double'),
    Field('weight_net', 'double'),
    Field('jar_type'),
)

db.olives.olive_kind.requires = IS_IN_SET({'k': 'Kalamata', 'l': 'Ligurian'})
db.olives.olive_kind.default = 'k'

db.olives.weight_tot.label = "Weight (gross)"
db.olives.weight_tot.requires=IS_FLOAT_IN_RANGE(
        0, 1000, error_message=T("Please enter a weigh in grams between 0 and 1Kg"))

db.olives.weight_net.label = "Weight (net, dry)"
db.olives.weight_net.requires=IS_FLOAT_IN_RANGE(
        0, 1000, error_message=T("Please enter a weigh in grams between 0 and 1Kg"))

db.commit()
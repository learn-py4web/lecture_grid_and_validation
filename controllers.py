"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.grid import Grid, GridClassStyleBulma

url_signer = URLSigner(session)

@action('index', method=['POST', 'GET']) # /fixtures_example/index
@action('index/<path:path>', method=['POST', 'GET']) # /fixtures_example/index
@action.uses(db, auth.user, 'index.html')
def index(path=None):
    grid = Grid(
        path,
        query=db.olives.id > 0,
        search_queries=None, search_form=None,
        editable=False, deletable=False, details=False, create=False,
        grid_class_style=GridClassStyleBulma,
        formstyle=FormStyleBulma,
    )
    return dict(grid=grid)


def validate_form_weights(form):
    """Checks that the gross weight is larger than the net weight."""
    if form.vars['weight_net'] > form.vars['weight_tot']:
        form.errors['weight_tot'] = T('The gross weight should be more than the net.')

@action('add', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'add.html')
def add():
    form = Form(db.olives, validation=validate_form_weights,
                csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('edit/<olives_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'edit.html')
def edit(olives_id=None):
    p = db.olives[olives_id]
    if p is None:
        redirect(URL('index'))
    form = Form(db.product, record=p, deletable=False,
                validation=validate_form_weights,
                csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

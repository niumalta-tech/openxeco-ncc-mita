from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs import fields

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access


class AddContact(MethodResource, Resource):

    def __init__(self, db):
        self.db = db

    @log_request
    @doc(tags=['contact'],
         description='Add a contact related to an entity',
         responses={
             "200": {},
             "422": {"description": "Provided entity not existing"},
         })
    @use_kwargs({
        'entity_id': fields.Int(),
        'user_id': fields.Int(),
        'type': fields.Str(),
        'representative': fields.Str(required=False, allow_none=True),
        'name': fields.Str(required=False, allow_none=True),
        'value': fields.Str(required=False, allow_none=True),
    })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def post(self, **kwargs):

        # Checking entity
        entity = self.db.get(self.db.tables["Entity"], {"id": kwargs["entity_id"]})

        if len(entity) == 0:
            return "", "422 Provided entity not existing"

        contacts = self.db.get(self.db.tables["EntityContact"], {"entity_id": kwargs["entity_id"]})

        if len(contacts) > 0:
            return "", "422 This entity already has a contact"

        # Insert
        self.db.insert(kwargs, self.db.tables["EntityContact"])

        return "", "200 "

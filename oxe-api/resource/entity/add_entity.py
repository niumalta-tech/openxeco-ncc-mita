import json
from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from webargs import fields

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access
from utils.serializer import Serializer


class AddEntity(MethodResource, Resource):

    db = None

    def __init__(self, db):
        self.db = db

    @log_request
    @doc(tags=['entity'],
         description='Add a entity. Return a dictionary with the data of the new object',
         responses={
             "200": {},
             "422": {"description": "A entity is already existing with that name"},
         })
    @use_kwargs({
        'name': fields.Str(),
    })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def post(self, **kwargs):

        entities = self.db.get(self.db.tables["Entity"], {"name": kwargs["name"]})

        if len(entities) > 0:
            return "", "422 A entity is already existing with that name"

        entity = self.db.insert(kwargs, self.db.tables["Entity"])

        try:
            self.db.insert({
                "entity_type": "Entity",
                "entity_id": entity.id,
                "action": "Create Entity",
                "values_before": "{}",
                "values_after": json.dumps(kwargs),
                "user_id": get_jwt_identity(),
            }, self.db.tables["AuditRecord"])
        except Exception as err:
            # We don't want the app to error if we can't log the action
            print(err)

        return Serializer.serialize(entity, self.db.tables["Entity"]), "200 "

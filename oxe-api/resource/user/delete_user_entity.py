from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs import fields

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access
from exception.object_not_found import ObjectNotFound


class DeleteUserEntity(MethodResource, Resource):

    def __init__(self, db):
        self.db = db

    @log_request
    @doc(tags=['user'],
         description='Delete an entity assignment to a user',
         responses={
             "200": {},
             "422": {"description": "Object not found"}
         })
    @use_kwargs({
        'user': fields.Int(),
        'entity': fields.Int(),
    })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def post(self, **kwargs):

        row = {
            "user_id": kwargs["user"],
            "entity_id": kwargs["entity"],
        }

        rights = self.db.get(self.db.tables["UserEntityAssignment"], row)

        if len(rights) > 0:
            self.db.delete(self.db.tables["UserEntityAssignment"], row)
        else:
            raise ObjectNotFound

        return "", "200 "

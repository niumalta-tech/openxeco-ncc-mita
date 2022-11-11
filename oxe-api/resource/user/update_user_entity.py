from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs import fields

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access
from exception.object_not_found import ObjectNotFound


class UpdateUserEntity(MethodResource, Resource):

    db = None

    def __init__(self, db):
        self.db = db

    @log_request
    @doc(tags=['user'],
         description='Update user group assignment',
         responses={
             "200": {},
             "422.a": {"description": "Object not found: group"},
             "422.b": {"description": "Object not found: user"}
         })
    @use_kwargs({
        'user': fields.Int(),
        'entity': fields.Int(),
        'department': fields.Str(allow_none=True),
    })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def post(self, **kwargs):

        user_entity_assignments = self.db.get(self.db.tables["UserEntityAssignment"], {
            "user_id": kwargs["user"],
            "entity_id": kwargs["entity"],
        })

        if len(user_entity_assignments) == 0:
            raise ObjectNotFound("UserEntityAssignment")

        self.db.merge({
            "user_id": kwargs["user"],
            "entity_id": kwargs["entity"],
            "department": kwargs["department"],
        }, self.db.tables["UserEntityAssignment"])

        return "", "200 "

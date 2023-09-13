from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs import fields

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access


class UpdateContact(MethodResource, Resource):

    db = None

    def __init__(self, db):
        self.db = db

    @log_request
    @doc(tags=['contact'],
         description='Update a contact related to an entity',
         responses={
             "200": {},
         })
    @use_kwargs({
        'id': fields.Int(),
        'entity_id': fields.Int(),
        'user_id': fields.Int(),
        'type': fields.Str(),
        'representative': fields.Str(required=False, allow_none=True),
        'name': fields.Str(required=False, allow_none=True),
        'value': fields.Str(required=False, allow_none=True),

        # 'department': fields.Str(required=False, allow_none=True),
        # 'seniority_level': fields.Str(required=False, allow_none=True),
        # 'work_email': fields.Str(required=False, allow_none=True),
        # 'work_telephone': fields.Str(required=False, allow_none=True),
    })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def post(self, **kwargs):

        self.db.merge(kwargs, self.db.tables["EntityContact"])

        return "", "200 "

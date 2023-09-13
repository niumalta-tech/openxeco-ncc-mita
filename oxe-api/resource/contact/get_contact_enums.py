from flask_apispec import MethodResource
from flask_apispec import doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from db.db import DB
from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access


class GetContactEnums(MethodResource, Resource):

    def __init__(self, db: DB):
        self.db = db

    @log_request
    @doc(tags=['contact'],
         description='Get enumerations of contact fields',
         responses={
             "200": {},
         })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def get(self):

        departments = self.db.get(self.db.tables['Department'])
        users = self.db.get(self.db.tables["User"], {"status": "ACCEPTED"})

        data = {
            "type": self.db.tables["EntityContact"].type.prop.columns[0].type.enums,
            "representative": self.db.tables["EntityContact"].representative.prop.columns[0].type.enums,
            "department": [department.name for department in departments],
            "user": [
                {
                    "id": user.id,
                    "full_name": f"{user.first_name} {user.last_name}",
                    "email": user.email,
                }
                for user in users
            ]
        }

        return data, "200 "

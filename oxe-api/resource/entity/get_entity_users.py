from flask_apispec import MethodResource
from flask_apispec import doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from db.db import DB
from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access


class GetEntityUsers(MethodResource, Resource):

    def __init__(self, db: DB):
        self.db = db

    @log_request
    @doc(tags=['entity'],
         description='Get the users assigned to an entity specified by its ID',
         responses={
             "200": {},
         })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def get(self, id_):
        entity_id = int(id_)
        query = (
            self.db.session.query(self.db.tables["UserEntityAssignment"])
            .join(self.db.tables["User"], self.db.tables["User"].id == self.db.tables["UserEntityAssignment"].user_id)
            .filter(
                self.db.tables["UserEntityAssignment"].entity_id == entity_id,
            )
        )

        users = query.with_entities(
            self.db.tables["User"].id,
            self.db.tables["User"].email,
            self.db.tables["User"].first_name,
            self.db.tables["User"].last_name,
            self.db.tables["UserEntityAssignment"].work_email
        ).all()

        return [user._asdict() for user in users], "200 "

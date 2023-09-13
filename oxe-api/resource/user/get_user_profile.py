from flask_apispec import MethodResource
from flask_apispec import doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from db.db import DB
from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access


class GetUserProfile(MethodResource, Resource):

    def __init__(self, db: DB):
        self.db = db

    @log_request
    @doc(tags=['private'],
         description='Get a user profile by user ID',
         responses={
             "200": {},
             "401": {"description": "Unauthorized"},
             "422": {"description": "Object not found"}
         })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def get(self, user_id):

        query = (
            self.db.session.query(self.db.tables["UserProfile"])
            .join(self.db.tables["User"], self.db.tables["User"].id == self.db.tables["UserProfile"].user_id)
            .filter(
                self.db.tables["UserProfile"].user_id == user_id,
            )
        )

        try:
            user, profile = query.with_entities(
                self.db.tables["User"],
                self.db.tables["UserProfile"],
            ).first()
        except TypeError as e:
            return "", "404 User has not completed their profile"

        profile = profile.__dict__
        del profile["_sa_instance_state"]

        profile["first_name"] = user.first_name
        profile["last_name"] = user.last_name
        profile["telephone"] = user.telephone

        return profile, "200 "

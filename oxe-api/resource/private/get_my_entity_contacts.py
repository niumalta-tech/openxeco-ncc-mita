from flask_apispec import MethodResource
from flask_apispec import doc
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from db.db import DB
from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from utils.serializer import Serializer


class GetMyEntityContacts(MethodResource, Resource):

    def __init__(self, db: DB):
        self.db = db

    @log_request
    @doc(tags=['private'],
         description='Get the list of contacts for a given entity',
         responses={
             "200": {},
         })
    @jwt_required
    @catch_exception
    def get(self, id_):

        entity_id = int(id_)

        query = (
            self.db.session.query(self.db.tables["EntityContact"])
            .join(self.db.tables["User"], self.db.tables["User"].id == self.db.tables["EntityContact"].user_id)
            .join(self.db.tables["UserEntityAssignment"], self.db.tables["UserEntityAssignment"].user_id == self.db.tables["EntityContact"].user_id)
            .filter(
                self.db.tables["EntityContact"].entity_id == entity_id,
                self.db.tables["UserEntityAssignment"].entity_id == entity_id,
            )
        )

        try:
            user, contact, assignment = query.with_entities(
                self.db.tables["User"],
                self.db.tables["EntityContact"],
                self.db.tables["UserEntityAssignment"],
            ).first()
        except TypeError as err:
            return "", "404 No Entity Contact"

        is_primary = int(get_jwt_identity()) == contact.user_id

        contact = {
            "name": f"{user.first_name} {user.last_name}",
            "work_email": assignment.work_email,
            "work_telephone": assignment.work_telephone,
            "seniority_level": assignment.seniority_level,
            "department": assignment.department,
            "acknowledged": "Yes",
            "primary": is_primary,
        }

        return contact, "200 "

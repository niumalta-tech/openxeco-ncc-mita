from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs import fields

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access


class UpdateProfile(MethodResource, Resource):

    db = None

    def __init__(self, db):
        self.db = db

    @log_request
    @doc(tags=['private'],
         description='Add a user profile',
         responses={
             "200": {},
             "422.a": {"description": "Object already existing"},
         })
    @use_kwargs({
        'user_id': fields.Int(),
        'data': fields.Dict(required=True, allow_none=False),
    })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def post(self, **kwargs):
        user_id = kwargs["user_id"]
        # db_profile = self.db.get(self.db.tables["UserProfile"], {"user_id": user_id})

        self.db.merge({
            'id': user_id,
            'first_name': kwargs["data"]['first_name'],
            'last_name': kwargs["data"]['last_name'],
            'telephone': kwargs["data"]['telephone'],
            'is_vcard_public': kwargs["data"]['public'],
            'status': "ACCEPTED",
        }, self.db.tables["User"])

        profile_data = {
            'user_id': user_id,
            'gender': kwargs["data"]['gender'],
            'sector': kwargs["data"]['sector'],
            'residency': kwargs["data"]['residency'],
            'mobile': kwargs["data"]['mobile'],
            'experience': kwargs["data"]['experience'],
            'domains_of_interest': kwargs["data"]['domains_of_interest'],
            'how_heard': kwargs["data"]['how_heard'],
            'profession_id': kwargs["data"]['profession_id'],
            'industry_id': kwargs["data"]['industry_id'],
            'nationality_id': kwargs["data"]['nationality_id'],
            'expertise_id': kwargs["data"]['expertise_id'],
            'public': kwargs["data"]['public'],
        }

        db_profile = self.db.get(self.db.tables["UserProfile"], {"user_id": user_id})

        if len(db_profile) > 0:
            profile_data['id'] = db_profile[0].id

        self.db.merge(profile_data, self.db.tables["UserProfile"])

        return "", "200 "

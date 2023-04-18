from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy import func
from webargs import fields, validate

from db.db import DB
from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access


class GetAcceptedUsers(MethodResource, Resource):

    def __init__(self, db: DB):
        self.db = db

    @log_request
    @doc(tags=['user'],
         description='Get users. The request returns a restricted amount of information '
                     '(id, email, is_admin, is_active, accept_communication)',
         responses={
             "200": {},
         })
    @use_kwargs({
        'page': fields.Int(required=False, missing=1, validate=validate.Range(min=1)),
        'per_page': fields.Int(required=False, missing=50, validate=validate.Range(min=1, max=50)),
        'date_from': fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=False),
        'date_to': fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=False),
    }, location="query")
    @jwt_required
    @verify_admin_access
    @catch_exception
    def get(self, **kwargs):

        request_query = (
            self.db.session.query( self.db.tables["UserRequest"])
            .join(self.db.tables["User"])
            .join(self.db.tables["UserProfile"], self.db.tables["UserRequest"].user_id == self.db.tables["UserProfile"].user_id)
            .join(self.db.tables["Country"])
            .join(self.db.tables["Profession"])
            .join(self.db.tables["Industry"])
            .join(self.db.tables["Expertise"])
            .filter(
                self.db.tables["UserRequest"].type == "NEW INDIVIDUAL ACCOUNT",
                self.db.tables["UserRequest"].status == "ACCEPTED",
            )
        )

        if "date_from" in kwargs:
            request_query = request_query.filter(self.db.tables["UserRequest"].submission_date >= kwargs["date_from"])

        if "date_to" in kwargs:
            request_query = request_query.filter(self.db.tables["UserRequest"].submission_date <= kwargs['date_to'])

        paginate = request_query.with_entities(
            self.db.tables["User"],
            self.db.tables["UserProfile"],
            self.db.tables["Country"],
            self.db.tables["Profession"],
            self.db.tables["Industry"],
            self.db.tables["Expertise"],
            self.db.tables["UserRequest"],
        ).paginate(kwargs['page'], kwargs['per_page'])
        # breakpoint()
        requests = [
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "telephone": user.telephone,
                "accept_communication": "Yes" if user.accept_communication == 1 else "No",
                "gender": user_profile.gender,
                "sector": user_profile.sector,
                "residency": user_profile.residency,
                "mobile": user_profile.mobile,
                "experience": user_profile.experience,
                "domains_of_interest": user_profile.domains_of_interest,
                "how_heard": user_profile.how_heard,
                "public": "Yes" if user_profile.public == 1 else "No",
                "profession": profession.name,
                "industry": industry.name,
                "nationality": country.name,
                "expertise": expertise.name,
                "submission_date": request.submission_date.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for (user, user_profile, country, profession, industry, expertise, request) in paginate.items
        ]

        return {
            "pagination": {
                "page": kwargs['page'],
                "pages": paginate.pages,
                "per_page": kwargs['per_page'],
                "total": paginate.total,
            },
            "items": requests,
        }, "200 "

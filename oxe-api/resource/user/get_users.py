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


class GetUsers(MethodResource, Resource):

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
        'ids': fields.DelimitedList(fields.Int(), required=False),
        'email': fields.Str(required=False),
        'page': fields.Int(required=False, missing=1, validate=validate.Range(min=1)),
        'per_page': fields.Int(required=False, missing=50, validate=validate.Range(min=1, max=50)),
        'admin_only': fields.Bool(required=False),
    }, location="query")
    @jwt_required
    @verify_admin_access
    @catch_exception
    def get(self, **kwargs):

        query = self.db.session.query(self.db.tables["User"])\
            .with_entities(self.db.tables["User"].id,
                           self.db.tables["User"].email,
                           self.db.tables["User"].is_admin,
                           self.db.tables["User"].is_active,
                           self.db.tables["User"].accept_communication) \
            .order_by(self.db.tables["User"].email.asc())

        if "ids" in kwargs:
            query = query.filter(self.db.tables["User"].id.in_(kwargs['ids']))

        if "email" in kwargs:
            query = query.filter(func.lower(self.db.tables["User"].email).like("%" + kwargs["email"] + "%"))

        if "admin_only" in kwargs and kwargs["admin_only"] is True:
            query = query.filter(self.db.tables["User"].is_admin.is_(True))

        paginate = query.paginate(kwargs['page'], kwargs['per_page'])
        users = [u._asdict() for u in paginate.items]

        return {
            "pagination": {
                "page": kwargs['page'],
                "pages": paginate.pages,
                "per_page": kwargs['per_page'],
                "total": paginate.total,
            },
            "items": users,
        }, "200 "

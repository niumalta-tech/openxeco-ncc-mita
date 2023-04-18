from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs import fields

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access


class DeleteCampaign(MethodResource, Resource):

    db = None

    def __init__(self, db):
        self.db = db

    @log_request
    @doc(tags=['campaign'],
         description='Delete a campaign',
         responses={
             "200": {},
             "422": {"description": "Provided campaign does not exist"},
         })
    @use_kwargs({
        'id': fields.Int(),
    })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def post(self, **kwargs):

        campaigns = self.db.get(self.db.tables["Campaign"], {"id": kwargs["id"]})

        if len(campaigns) == 0:
            return "", "422 Provided campaign does not exist"

        self.db.delete(
            self.db.tables["Campaign"],
            {"id": kwargs["id"]}
        )

        return "", "200 "

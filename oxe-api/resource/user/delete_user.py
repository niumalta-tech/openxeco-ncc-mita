import datetime
from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs import fields
from flask import request, render_template
from flask_jwt_extended import create_access_token

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access
from exception.object_not_found import ObjectNotFound
from utils.mail import send_email


class DeleteUser(MethodResource, Resource):

    db = None

    def __init__(self, db, mail):
        self.db = db
        self.mail = mail

    @log_request
    @doc(tags=['user'],
         description='Delete a user',
         responses={
             "200": {},
             "422": {"description": "Object not found"}
         })
    @use_kwargs({
        'id': fields.Int(),
    })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def post(self, **kwargs):

        if 'HTTP_ORIGIN' in request.environ and request.environ['HTTP_ORIGIN']:
            origin = request.environ['HTTP_ORIGIN']
        else:
            return "", "500 Impossible to find the origin. Please contact the administrator"


        entities = self.db.get(self.db.tables["User"], {"id": kwargs["id"]})

        if len(entities) > 0:
            # self.db.delete(self.db.tables["User"], {"id": kwargs["id"]})
            print("test")
        else:
            raise ObjectNotFound

        user = entities[0]
        expires = datetime.timedelta(minutes=15)
        token = create_access_token(str(user.id), expires_delta=expires)
        url = f"{origin}/verify_delete_user?token={token}"

        send_email(
            self.mail,
            subject=f"Confirm Delete Account",
            recipients=[user.email],
            html_body=render_template(
                'account_deletion.html',
                url=url,
            )
        )

        return "", "200 "
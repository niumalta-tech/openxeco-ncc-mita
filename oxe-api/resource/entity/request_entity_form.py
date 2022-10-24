from flask import request, render_template
from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from webargs import fields

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from utils.mail import send_email_with_attachment
from utils.re import has_mail_format
from utils.token import generate_confirmation_token

class RequestEntityForm(MethodResource, Resource):

    db = None
    mail = None

    def __init__(self, db, mail):
        self.db = db
        self.mail = mail

    @log_request
    @doc(tags=['entity'],
         description='Request a entity registration form',
         responses={
             "200": {},
             "422.a": {"description": "The provided email does not have the right format"},
             "422.b": {"description": "An account already exists with this email address"},
             "422.c": {"description": "Object already existing"},
             "500": {"description": "Impossible to find the origin. Please contact the administrator"},
         })
    @use_kwargs({
        'email': fields.Str(),
    })
    @jwt_required
    @catch_exception
    def post(self, **kwargs):

        email = kwargs["email"].lower()

        if 'HTTP_ORIGIN' in request.environ and request.environ['HTTP_ORIGIN']:
            origin = request.environ['HTTP_ORIGIN']
        else:
            return "", "500 Impossible to find the origin. Please contact the administrator"

        if not has_mail_format(email):
            return "", "422 The provided email does not have the right format"

        # Get user
        user = self.db.get(self.db.tables["User"], {"id": get_jwt_identity()})
        if len(user) == 0:
            return "", "401 The user has not been found"
        user = user[0].__dict__
    
        self.db.merge(
            {
                "id": get_jwt_identity(),
                "work_email": kwargs["email"]
            },
            self.db.tables["User"]
        )



        # Send email
        token = generate_confirmation_token(kwargs["email"])
        try:
            url = f"{origin}/add_entity?tab=register&action=verify_register&token={token}"
            send_email_with_attachment(self.mail,
                subject="Entity Registration Request",
                recipients=[email],
                html_body=render_template(
                    'entity_registration.html',
                    first_name=user["first_name"],
                    url=url,
                ),
                file_name="Entity Registration - Signatory Approval.pdf",
                file_type="application/pdf",
            )
        except Exception as e:
            raise e

        return "", "200"

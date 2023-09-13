from flask import render_template
from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorator.verify_admin_access import verify_admin_access
from flask_restful import Resource
from flask_bcrypt import check_password_hash
from webargs import fields

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from utils.mail import send_email


class DisassociateUserEntity(MethodResource, Resource):

    db = None
    mail = None

    def __init__(self, db, mail):
        self.db = db
        self.mail = mail

    @log_request
    @doc(tags=['user'],
         description='Disassociate a user from and Entity',
         responses={
             "200": {"description": "User unlinked from Entity"},
             "401.a": {"description": "Incorrect password"},
             "422": {"description": "No entity association found"}
         })
    @use_kwargs({
        'user_id': fields.Int(),
        'entity_id': fields.Int(),
    })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def post(self, **kwargs):
        # Check if the password is correct
        users = self.db.get(self.db.tables["User"], {"id": kwargs["user_id"]})
        user = users[0]

        entity = self.db.get(self.db.tables["Entity"], {"id": kwargs["entity_id"]})[0]

        row = {
            "user_id": kwargs["user_id"],
            "entity_id": kwargs["entity_id"],
        }

        # Delete Assignment
        assignments = self.db.get(self.db.tables["UserEntityAssignment"], row)
        if len(assignments) > 0:
            self.db.delete(self.db.tables["UserEntityAssignment"], row)
        else:
            return "", "422 No entity association found"

        # check if primary
        contact = self.db.get(self.db.tables["EntityContact"], row)
        is_primary = len(contact) > 0

        # If primary
        if is_primary:
            self.db.delete(self.db.tables["EntityContact"], row)
            bcc_addresses = self.db.session \
                .query(self.db.tables["User"]) \
                .with_entities(self.db.tables["User"].email) \
                .filter(self.db.tables["User"].is_admin.is_(True)) \
                .filter(self.db.tables["User"].is_active.is_(True)) \
                .filter(self.db.tables["User"].accept_request_notification.is_(True)) \
                .all()
            bcc_addresses = [a[0] for a in bcc_addresses]

            # email company and cc mita
            send_email(self.mail,
                subject=f"User Disassociated from {entity.name}",
                recipients=[entity.email],
                bcc=bcc_addresses,
                html_body=render_template(
                    'disassociated_from_entity_notify.html',
                    email=entity.email,
                    user_email=contact[0].value,
                    entity=entity.name,
                    primary='yes'
                )
            )
        else:
            contacts = self.db.get(self.db.tables["EntityContact"], {"entity_id": kwargs["entity_id"]})
            if contacts:
                contact_user = data = self.db.get(self.db.tables["User"], {"id": contacts[0].user_id})
                send_email(self.mail,
                    subject=f"User Disassociated from {entity.name}",
                    recipients=[contact_user[0].email],
                    html_body=render_template(
                        'disassociated_from_entity_notify.html',
                        email=entity.email,
                        user_email=user.email,
                        entity=entity.name,
                        primary='no'
                    )
                )

        send_email(self.mail,
            subject=f"User Disassociated from {entity.name}",
            recipients=[user.email],
            html_body=render_template(
                'disassociated_from_entity_user.html',
                email=user.email,
                entity=entity.name,
            )
        )

        return "", "200"

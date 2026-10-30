import re

from flask import Blueprint, current_app, request
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError

from api.authorize import token_required
from model.volunteers import (
    VolunteerApplication,
    createVolunteerApplication,
    getVolunteerApplications,
)


volunteer_api = Blueprint("volunteer_api", __name__, url_prefix="/api/volunteers")
api = Api(volunteer_api)

VOLUNTEER_ROLES = {
    "Research & Education",
    "Webmaster",
    "Tool Kit Assembly leader",
    "Community Outreach & Events",
    "Video Content Creator",
    "I'm open to any role",
}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class VolunteerAPI:
    class _Applications(Resource):
        def post(self):
            data = request.get_json(silent=True)
            if not isinstance(data, dict):
                return {"message": "A JSON object is required."}, 400

            name = data.get("name")
            email = data.get("email")
            role_interest = data.get("role")
            message = data.get("message", "")

            if not isinstance(name, str) or not 2 <= len(name.strip()) <= 255:
                return {"message": "Name must be between 2 and 255 characters."}, 400
            if (
                not isinstance(email, str)
                or len(email.strip()) > 320
                or not EMAIL_PATTERN.fullmatch(email.strip())
            ):
                return {"message": "A valid email address is required."}, 400
            if not isinstance(role_interest, str) or role_interest not in VOLUNTEER_ROLES:
                return {"message": "Choose a valid volunteer role."}, 400
            if not isinstance(message, str) or len(message) > 2000:
                return {"message": "Message must be 2000 characters or fewer."}, 400

            application = VolunteerApplication(
                name=name.strip(),
                email=email.strip(),
                role_interest=role_interest,
                message=message.strip() or None,
            )
            try:
                createVolunteerApplication(application)
            except SQLAlchemyError:
                current_app.logger.exception("Failed to save volunteer application")
                return {"message": "Unable to save the application right now."}, 500

            return application.read(), 201

        @token_required("Admin")
        def get(self):
            applications = getVolunteerApplications()
            return [application.read() for application in applications]

    api.add_resource(_Applications, "", "/")

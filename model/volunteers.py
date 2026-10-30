from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError

from __init__ import db


class VolunteerApplication(db.Model):
    __tablename__ = "volunteer_applications"

    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(320), primary_key=True, nullable=False)
    role_interest = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        primary_key=True,
        nullable=False,
    )
    status = db.Column(db.String(20), default="Pending", nullable=False)

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def read(self):
        return {
            "name": self.name,
            "email": self.email,
            "role_interest": self.role_interest,
            "message": self.message,
            "submitted_at": self.submitted_at.replace(tzinfo=timezone.utc).isoformat(),
            "status": self.status,
        }


def createVolunteerApplication(application):
    return application.create()


def getVolunteerApplications():
    return VolunteerApplication.query.order_by(
        VolunteerApplication.submitted_at.desc()
    ).all()

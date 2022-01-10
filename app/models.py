import functools
import typing as t
from datetime import datetime

from sqlalchemy.sql.schema import Column as SAColumn

from app import db


# Make columns not nullable by default
# noinspection PyTypeChecker
Column: t.Type[SAColumn] = functools.partial(SAColumn, nullable=False)


class BaseModel(db.Model):
    """
    Base model for all model classes.
    Automatically adds created_at and modified_at columns.
    """
    __abstract__ = True

    created_at = Column(db.DateTime, index=True, default=db.func.now())
    modified_at = Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=True)


"""M2M relationship table between Candidate and Skill."""
candidate_skills = db.Table('candidate_skills',
    db.Column('candidate_id', db.Integer, db.ForeignKey('candidate.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)


class Candidate(BaseModel):
    """A candidate for a job."""
    id = Column(db.Integer, primary_key=True)
    first_name = Column(db.String(40))
    surname = Column(db.String(40))
    email = Column(db.String(100))
    phone_number = Column(db.String(20), nullable=True)
    expected_salary = Column(db.Integer)
    skills = db.relationship('Skill', secondary=candidate_skills, lazy='dynamic',
                             backref=db.backref('candidates', lazy='dynamic'))
    applications = db.relationship('JobApplication', lazy='dynamic', back_populates="candidate",
                                   cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return '<Candidate {} {}>'.format(self.first_name, self.surname)


class JobApplication(BaseModel):
    """
    A M2M relationship between Job and Candidate representing a job application.
    Created as a separate model class since it is likely to contain additional fields, such as application_status.
    """
    id = Column(db.Integer, primary_key=True)
    candidate_id = Column(db.Integer, db.ForeignKey('candidate.id', ondelete="CASCADE"))
    advertisement_id = Column(db.Integer, db.ForeignKey('job_advertisement.id', ondelete="CASCADE"))
    candidate = db.relationship('Candidate', back_populates="applications")
    advertisement = db.relationship('JobAdvertisement', back_populates="applications")

    def __repr__(self):
        return '<JobApplication {}>'.format(self.id)


class Skill(BaseModel):
    """A skill that a candidate can have."""
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(60))

    def __repr__(self):
        return '<Skill {}>'.format(self.name)

    @classmethod
    def bulk_get_or_create(cls, skill_names: t.List[str]) -> t.List['Skill']:
        """
        Get list of skill objects corresponding to passed skill_names, creating those that do not yet exist.
        """
        existing = cls.query.filter(cls.name.in_(skill_names)).all()
        existing_names = [skill.name for skill in existing]

        new_skills = [Skill(name=name) for name in set(skill_names) - set(existing_names)]
        db.session.add_all(new_skills)

        return existing + new_skills


class JobAdvertisement(BaseModel):
    """A job advertisement that candidates can apply for."""
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(60))
    salary_min = Column(db.Integer)
    salary_max = Column(db.Integer)
    full_text = Column(db.Text)
    applications = db.relationship('JobApplication',  lazy='dynamic', back_populates="advertisement",
                                   cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return '<JobAdvertisement {}>'.format(self.title)

    def get_candidates(self):
        """Returns a list of all candidates that applied for this job advertisement."""
        return [a.candidate for a in self.applications.all()]

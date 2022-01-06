import functools
import typing as t
from datetime import datetime

from sqlalchemy.sql.schema import Column as SAColumn

from app import db


# Make columns not nullable by default
# noinspection PyTypeChecker
Column: t.Type[SAColumn] = functools.partial(SAColumn, nullable=False)


class BaseModel(db.Model):
    __abstract__ = True

    created_at = Column(db.DateTime, index=True, default=db.func.now())
    modified_at = Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=True)


candidate_skills = db.Table('candidate_skills',
    db.Column('candidate_id', db.Integer, db.ForeignKey('candidate.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)


class Candidate(BaseModel):
    id = Column(db.Integer, primary_key=True)
    first_name = Column(db.String(40))
    surname = Column(db.String(40))
    email = Column(db.String(100))
    phone_number = Column(db.String(20), nullable=True)
    expected_salary = Column(db.Integer)
    advertisement_id = Column(db.Integer, db.ForeignKey('job_advertisement.id'), nullable=True)
    skills = db.relationship('Skill', secondary=candidate_skills, lazy='dynamic',
                             backref=db.backref('candidates', lazy='dynamic'))

    def __repr__(self):
        return '<Candidate {} {}>'.format(self.first_name, self.surname)


class Skill(BaseModel):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(60))

    def __repr__(self):
        return '<Skill {}>'.format(self.name)


class JobAdvertisement(BaseModel):
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(60))
    salary_min = Column(db.Integer)
    salary_max = Column(db.Integer)
    full_text = Column(db.Text)
    candidates = db.relationship('Candidate', backref='advertisement', lazy=True)

    def __repr__(self):
        return '<JobAdvertisement {}>'.format(self.title)

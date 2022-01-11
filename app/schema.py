from app import ma
from app.models import Candidate, JobAdvertisement, JobApplication, Skill


class SkillSchema(ma.SQLAlchemyAutoSchema):
    """Schema for the Skill model."""
    class Meta:
        model = Skill
        fields = ("id", "name")


class CandidateSchema(ma.SQLAlchemyAutoSchema):
    """Schema for the Candidate model."""
    class Meta:
        model = Candidate
        # fail-safe selection of model fields
        fields = ("id", "first_name", "surname", "email", "phone_number",
                  "expected_salary", "advertisement", "skills")

    # override to include proper validation
    email = ma.Email(required=True)
    skills = ma.Nested(SkillSchema, many=True)


class JobAdvertisementSchema(ma.SQLAlchemyAutoSchema):
    """Schema for the JobAdvertisement model."""
    class Meta:
        model = JobAdvertisement
        fields = ("id", "title", "salary_min", "salary_max", "full_text",)


class JobApplicationSchema(ma.SQLAlchemyAutoSchema):
    """Schema for the JobApplication model."""
    class Meta:
        model = JobApplication
        fields = ("id", "candidate_id", "application_id")


# Schema object definitions

candidate_schema = CandidateSchema()
candidates_schema = CandidateSchema(many=True)
advertisement_schema = JobAdvertisementSchema()
advertisements_schema = JobAdvertisementSchema(many=True)
applications_schema = JobApplicationSchema(many=True)
skills_schema = SkillSchema(many=True)

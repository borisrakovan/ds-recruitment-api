from flask import request
from marshmallow import ValidationError
from app.schema import candidate_schema, candidates_schema, advertisement_schema, advertisements_schema, \
    applications_schema
from app import utils, crud
from ds_recruitment_api import app

from app import db
from app.errors import error_response
from app.models import Candidate, Skill, JobAdvertisement, JobApplication


@app.route('/', methods=["GET"])
def health():
    return f'Hi! Datasentics recruitment API is live.', 200


# Candidates


@app.route('/candidates', methods=['POST'])
def create_candidate():
    """Create a new candidate and return it."""
    if (data := request.get_json()) is None:
        return error_response(400, "No input data provided.")

    if 'skills' not in data:
        return error_response(422, "Missing parameter: 'skills'.")

    skill_names = data['skills']
    del data['skills']

    if not isinstance(skill_names, list):
        return error_response(422, "Parameter 'skills' must be a list.")

    try:
        data = candidate_schema.load(data)
    except ValidationError as err:
        return error_response(422, err.messages)

    candidate = Candidate(**data)
    db.session.add(candidate)

    skills = Skill.bulk_get_or_create(skill_names)

    candidate.skills.extend(skills)
    db.session.commit()

    candidate_dict = candidate_schema.dump(candidate)
    return {'result': candidate_dict}, 201


@app.route('/candidates', methods=['GET'])
def read_all_candidates():
    """Get all candidates."""
    return crud.read_all(Candidate, candidates_schema)


@app.route('/candidates/<int:candidate_id>', methods=['GET'])
def read_candidate(candidate_id: int):
    """Get candidate by ID."""
    return crud.read(Candidate, candidate_schema, candidate_id)


@app.route('/candidates/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id: int):
    """
    Update an existing candidate by ID.
    Return the updated candidate.
    """
    if (data := request.get_json()) is None:
        return error_response(400, "No input data provided.")

    if 'skills' not in data:
        return error_response(422, "Missing parameter: 'skills'.")

    skill_names = data['skills']
    del data['skills']

    if not isinstance(skill_names, list):
        return error_response(422, "Parameter 'skills' must be a list.")

    try:
        data = candidate_schema.load(data)
    except ValidationError as err:
        return error_response(422, err.messages)

    if (candidate := Candidate.query.get(candidate_id)) is None:
        return error_response(404, "Candidate not found.")

    # ID is immutable, make sure we don't accidentally change it
    if 'id' in data:
        del data['id']

    utils.update_object_from_dict(candidate, data)

    skills = Skill.bulk_get_or_create(skill_names)
    candidate.skills = skills

    db.session.commit()

    return {'result': candidate_schema.dump(candidate)}


@app.route('/candidates/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id: int):
    """Delete candidate by ID."""
    return crud.delete(Candidate, candidate_id)


# Advertisements


@app.route('/advertisements', methods=['POST'])
def create_advertisement():
    """Create a new advertisement and return it."""
    if (data := request.get_json()) is None:
        return error_response(400, "No input data provided.")

    try:
        data = advertisement_schema.load(data)
    except ValidationError as err:
        return error_response(422, err.messages)

    if data['salary_min'] > data['salary_max']:
        return error_response(422, "Salary min must be lower or equal to salary max.")

    advertisement = JobAdvertisement(**data)
    db.session.add(advertisement)
    db.session.commit()

    return {'result': advertisement_schema.dump(advertisement)}, 201


@app.route('/advertisements', methods=['GET'])
def read_all_advertisements():
    """Get all advertisements."""
    return crud.read_all(JobAdvertisement, advertisements_schema)


@app.route('/advertisements/<int:advertisement_id>', methods=['GET'])
def read_advertisement(advertisement_id: int):
    """Get advertisement and its applications by ID."""
    return crud.read(JobAdvertisement, advertisement_schema, advertisement_id)


@app.route('/advertisements/<int:advertisement_id>', methods=['PUT'])
def update_advertisement(advertisement_id: int):
    """
    Update an existing advertisement by ID.
    Return the updated advertisement.
    """
    if (data := request.get_json()) is None:
        return error_response(400, "No input data provided.")

    try:
        data = advertisement_schema.load(data)
    except ValidationError as err:
        return error_response(422, err.messages)

    if (advertisement := JobAdvertisement.query.get(advertisement_id)) is None:
        return error_response(404, "Advertisement not found.")

    # ID is immutable, make sure we don't accidentally change it
    if 'id' in data:
        del data['id']

    obj_changed = utils.update_object_from_dict(advertisement, data)
    if obj_changed:
        db.session.commit()

    return {'result': advertisement_schema.dump(advertisement)}


@app.route('/advertisements/<int:advertisement_id>', methods=['DELETE'])
def delete_advertisement(advertisement_id: int):
    """Delete advertisement by ID."""
    return crud.delete(JobAdvertisement, advertisement_id)


# Other endpoints


@app.route('/advertisements/<int:advertisement_id>/apply', methods=['POST'])
def apply_for_advertisement(advertisement_id: int):
    """
    Apply for an advertisement by ID.
    Return the updated advertisement along with its candidates.
    """
    if (data := request.get_json()) is None:
        return error_response(400, "No input data provided.")

    if 'candidate_id' not in data:
        return error_response(400, "Missing parameter: candidate_id.")

    if (advertisement := JobAdvertisement.query.get(advertisement_id)) is None:
        return error_response(404, "Advertisement not found.")

    if (candidate := Candidate.query.get(data['candidate_id'])) is None:
        return error_response(404, "Candidate not found.")

    if candidate in advertisement.get_candidates():
        return error_response(400, "Candidate already applied.")

    application = JobApplication(candidate=candidate, advertisement=advertisement)
    db.session.add(application)
    db.session.commit()

    advertisement_dict = advertisement_schema.dump(advertisement)
    advertisement_dict['applications'] = applications_schema.dump(advertisement.applications)
    return {'result': advertisement_dict}

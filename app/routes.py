from flask import jsonify, request

from app.schema import candidate_schema, candidates_schema, advertisement_schema, advertisements_schema
from app.utils import update_object_from_dict
from ds_recruitment_api import app
from marshmallow import ValidationError

from app import db
from app.errors import error_response
from app.models import Candidate, Skill, JobAdvertisement


@app.route('/', methods=["GET"])
def test():
    return f'Hi! Debug: {app.config["DEBUG"]}'


"""Candidates"""


@app.route('/candidates', methods=['POST'])
def create_candidate():
    """Create a new candidate and return it."""
    if (data := request.get_json()) is None:
        return error_response(400, "No input data provided.")

    try:
        data = candidate_schema.load(data)
    except ValidationError as err:
        return error_response(422, err.messages)

    candidate = Candidate(**data)
    db.session.add(candidate)
    db.session.commit()

    return {'candidate': candidate_schema.dump(candidate)}, 201


@app.route('/candidates', methods=['GET'])
def read_all_candidates():
    """Get all candidates."""
    candidates = Candidate.query.all()
    return {'candidates': candidates_schema.dump(candidates)}


@app.route('/candidates/<int:candidate_id>', methods=['GET'])
def read_candidate(candidate_id: int):
    """Get candidate by ID."""

    if (candidate := Candidate.query.get(candidate_id)) is None:
        return error_response(404, "Candidate not found.")

    return {'candidate': candidate_schema.dump(candidate)}


@app.route('/candidates/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id: int):
    """
    Update an existing candidate by ID.
    Return the updated candidate.
    """
    if (data := request.get_json()) is None:
        return error_response(400, "No input data provided.")

    try:
        data = candidate_schema.load(data)
    except ValidationError as err:
        return error_response(422, err.messages)

    if (candidate := Candidate.query.get(candidate_id)) is None:
        return error_response(404, "Candidate not found.")

    # ID is immutable, make sure we don't accidentally change it
    if 'id' in data:
        del data['id']

    obj_changed = update_object_from_dict(candidate, data)
    if obj_changed:
        db.session.commit()

    return {'candidate': candidate_schema.dump(candidate)}


@app.route('/candidates/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id: int):
    """Delete candidate by ID."""
    candidate = Candidate.query.get(candidate_id)

    if candidate is None:
        return error_response(404, "Candidate not found.")

    db.session.delete(candidate)
    db.session.commit()
    return '', 204


"""Advertisements"""


@app.route('/advertisements', methods=['POST'])
def create_advertisement():
    """Create a new advertisement and return it."""
    if (data := request.get_json()) is None:
        return error_response(400, "No input data provided.")

    try:
        data = advertisement_schema.load(data)
    except ValidationError as err:
        return error_response(422, err.messages)

    advertisement = JobAdvertisement(**data)
    db.session.add(advertisement)
    db.session.commit()

    return {'advertisement': advertisement_schema.dump(advertisement)}, 201


@app.route('/advertisements', methods=['GET'])
def read_all_advertisements():
    """Get all advertisements."""
    advertisements = JobAdvertisement.query.all()
    return {'advertisements': advertisements_schema.dump(advertisements)}


@app.route('/advertisements/<int:advertisement_id>', methods=['GET'])
def read_advertisement(advertisement_id: int):
    """Get advertisement by ID."""

    if (advertisement := JobAdvertisement.query.get(advertisement_id)) is None:
        return error_response(404, "Advertisement not found.")

    return {'advertisement': advertisement_schema.dump(advertisement)}


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

    obj_changed = update_object_from_dict(advertisement, data)
    if obj_changed:
        db.session.commit()

    return {'advertisement': advertisement_schema.dump(advertisement)}


@app.route('/advertisements/<int:advertisement_id>', methods=['DELETE'])
def delete_advertisement(advertisement_id: int):
    """Delete advertisement by ID."""
    advertisement = JobAdvertisement.query.get(advertisement_id)

    if advertisement is None:
        return error_response(404, "Advertisement not found.")

    db.session.delete(advertisement)
    db.session.commit()
    return '', 204

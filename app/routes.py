from flask import jsonify, request

from app.schema import candidate_schema, candidates_schema
from ds_recruitment_api import app
from marshmallow import ValidationError

from app import db
from app.errors import error_response
from app.models import Candidate, Skill, JobAdvertisement


@app.route('/', methods=["GET"])
def test():
    return f'Hi! Debug: {app.config["DEBUG"]}'


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

    candidate = Candidate.query.get(candidate_id)
    # todo: error_response

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

    candidate = Candidate.query.get(candidate_id)
    # todo: error_response
    print(type(data))
    candidate.name = data['name']
    candidate.description = data['description']
    db.session.commit()

    return {'candidate': candidate_schema.dump(candidate)}


@app.route('/candidates/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id: int):
    """Delete candidate by ID."""
    # todo
    candidate = Candidate.query.get_or_404(candidate_id)
    db.session.delete(candidate)
    db.session.commit()
    return '', 204

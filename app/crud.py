import typing as t
from flask_marshmallow.sqla import SQLAlchemySchema

from app import db
from app.errors import error_response
from app.models import BaseModel


def read(model_cls: t.Type[BaseModel], model_schema: SQLAlchemySchema, instance_id: int):
    """Utility handler for "read instance of model_cls" endpoint."""
    if (instance := model_cls.query.get(instance_id)) is None:
        return error_response(404, f"{model_cls.__name__} not found.")

    return {'result': model_schema.dump(instance)}


def read_all(model_cls: t.Type[BaseModel], many_schema: SQLAlchemySchema):
    """Utility handler for "read all instances of model_cls" endpoint."""
    instances = model_cls.query.all()
    return {'result': many_schema.dump(instances)}


def delete(model_cls: t.Type[BaseModel], instance_id: int):
    """Utility handler for endpoint providing a simple deletion of a model_cls instance."""
    instance = model_cls.query.get(instance_id)

    if instance is None:
        return error_response(404, f"{model_cls.__name__} not found.")

    db.session.delete(instance)
    db.session.commit()
    return '', 204

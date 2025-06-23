from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db import get_db


class BaseService(object):

    model = None
    db = None

    def __init__(self, db: Session):
        self.db = db

    def create(self, create_schema):

        model = self.model()
        for field_name, value in create_schema.dict(exclude_unset=True).items():
            setattr(model, field_name, value)

        self.db.add(model)
        try:
            self.db.commit()
        except Exception as e:

            # this is general exception catching and if needed this logic can be extended to log it somewhere
            print("Exception type:", type(e))
            print("Exception class name:", type(e).__name__)
            print("Error occured during creation of:", self.model.__name__)
            self.db.rollback()
            # raises exception thrown, so children can catch them and act accordingly
            raise e

        self.db.refresh(model)
        return model

    def get_by_id(self, entity_id):

        entity = self.db.query(self.model).filter(self.model.id == entity_id).first()
        return entity

    def delete(self, entity_id: int):
        entity = self.db.query(self.model).filter(self.model.id == entity_id).first()
        if not entity:
            return False
        self.db.delete(entity)
        self.db.commit()
        return True

    def update(self, entity_id, update_schema):
        existing_entity = self.db.query(self.model).filter(self.model.id == entity_id).first()

        try:
            for field_name, value in update_schema.dict(exclude_unset=True).items():
                setattr(existing_entity, field_name, value)
            self.db.commit()
            self.db.refresh(existing_entity)
        except Exception as e:
            self.db.rollback()
            raise e
        return existing_entity

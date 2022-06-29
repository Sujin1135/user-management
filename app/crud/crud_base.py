import logging
from typing import TypeVar, Generic, Type, Union, Any, Dict
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from app.models.base import Base
from app.core.db import get_db_session
from app.exceptions.duplication_error import DuplicationError
from app.exceptions.not_found_error import NotFoundError
from sqlalchemy.sql.expression import ColumnElement
from datetime import datetime

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_last(self) -> ModelType:
        session = get_db_session()
        try:
            return (
                session.query(self.model)
                .filter(self.model.deleted_at == None)
                .order_by(self.model.id.desc())
                .first()
            )
        except Exception as e:
            logging.error("failed to get a last model", e)
            raise e
        finally:
            session.close()

    def get(self, model_id: int) -> ModelType:
        try:
            session = get_db_session()
            target = session.query(self.model).filter(self.model.id == model_id).first()

            NotFoundError.validate_exists(target)

            return target
        except IntegrityError as e:
            logging.error("*** occurred a mysql error when get a model by id")
            raise e
        finally:
            session.close()

    def create(self, create_schema: CreateSchemaType) -> ModelType:
        params = jsonable_encoder(create_schema)
        model = self.model(**params)
        db_session = get_db_session()

        try:
            db_session.add(model)
            db_session.commit()
            db_session.refresh(model)
            return model
        except IntegrityError as e:
            logging.error("*** occurred a mysql error when create a model as below")

            if DuplicationError.is_duplication_err(e):
                raise DuplicationError("중복된 키값이 존재합니다")

            raise e
        except Exception as e:
            logging.error("*** occurred unknown error when create a model")
            raise e
        finally:
            db_session.close()

    def _get_update_params(
        self, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> dict:
        return obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)

    def _validate_update(self, params: dict):
        param_keys = params.keys()
        model_keys = self.model.__dict__.keys()
        for k in param_keys:
            if k not in model_keys:
                raise ValueError("올바르지 않은 프로퍼티가 포함되어 있습니다. {}".format(k))

    def _inject_param_values(self, model: ModelType, params: dict) -> None:
        keys = list(filter(lambda x: params[x] is not None, params.keys()))
        for k in keys:
            setattr(model, k, params[k])

    def _parse_schedule_find_query(self, query_dict):
        q = tuple(
            map(
                lambda k: getattr(self.model, k) == query_dict[k],
                filter(
                    lambda k: query_dict[k] is not None,
                    query_dict.keys(),
                ),
            )
        )
        return q

    def update(
        self, model_id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        encoded = jsonable_encoder(obj_in)
        params = self._get_update_params(encoded)

        self._validate_update(params)

        db_session = get_db_session()
        model = db_session.query(self.model).get(model_id)

        NotFoundError.validate_exists(model)

        self._inject_param_values(model, params)

        try:
            db_session.add(model)
            db_session.commit()
            db_session.refresh(model)
            return model
        except Exception as e:
            logging.error("*** occurred a mysql error when update a model as below")
            if NotFoundError.is_not_foreign_key_existed(e):
                raise NotFoundError(f"해당 데이터가({model_id}) 존재하지 않습니다")
            raise e
        finally:
            db_session.close()

    def remove(self, model_id: int) -> ModelType:
        db_session = get_db_session()
        try:
            model = db_session.query(self.model).get(model_id)

            if model is None:
                raise NotFoundError("데이터가 존재하지 않습니다")

            db_session.delete(model)
            db_session.commit()
            return model
        except Exception as e:
            logging.error("*** occurred a mysql error when delete a model as below")
            raise e
        finally:
            db_session.close()

    def soft_remove(self, model_id: int) -> None:
        db_session = get_db_session()
        try:
            model = db_session.query(self.model).get(model_id)

            NotFoundError.validate_exists(model)

            db_session.query(self.model).filter(self.model.id == model_id).update(
                {"deleted_at": datetime.now()}
            )

            db_session.commit()
        except Exception as e:
            logging.error("*** occurred a mysql error when delete a model as below")
            raise e
        finally:
            db_session.close()

    def find(
        self,
        queries: dict = {},
        order_by: ColumnElement = None,
        offset: int = 0,
        limit: int = 50,
    ) -> list:
        order_by = asc(self.model.id) if order_by is None else order_by
        try:
            parsed_queries = self._parse_schedule_find_query(query_dict=queries)
            session = get_db_session()
            data = (
                session.query(self.model)
                .filter(*parsed_queries)
                .filter(self.model.deleted_at == None)
                .order_by(order_by)
                .limit(limit)
                .offset(offset)
                .all()
            )
            return data

        except Exception as e:
            logging.error("*** occurred a mysql error when find a model as below")
            raise e
        finally:
            session.close()

    def find_with_deleted(
        self,
        queries: dict = {},
        order_by: ColumnElement = None,
        limit: int = 50,
        offset: int = 0,
    ):
        order_by = asc(self.model.id) if order_by is None else order_by
        try:
            parsed_queries = self._parse_schedule_find_query(query_dict=queries)
            session = get_db_session()
            data = (
                session.query(self.model)
                .filter(*parsed_queries)
                .order_by(order_by)
                .limit(limit)
                .offset(offset)
                .all()
            )
            return data
        except Exception as e:
            logging.error("*** occurred a mysql error when find a model as below")
            raise e
        finally:
            session.close()

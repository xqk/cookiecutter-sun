import math
from typing import Type, Dict

from sun.db import db
from sun.schema import model_to_schema
from sun.db.operators import dj_lookup_to_sqla, dj_ordering_to_sqla
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import func

from consts import ALWAYS_EXCLUDE
from schemas.generic_rpc import BulkCreateRequest

__all__ = ["ModelBiz", "clean"]
READONLY_FIELDS = {"id", "{{cookiecutter.business_key}}", "created_time", "updated_time", "limit", "offset", "ordering"}


def clear_readonly_fields(data: Dict) -> Dict:
    return {k: v for k, v in data.items() if k not in READONLY_FIELDS}


def flat_data(data: Dict) -> Dict:
    if len(data) == 1 and isinstance(data.get("data"), dict):
        data = data["data"]
    return data


clean_steps = (
    clear_readonly_fields,
    flat_data,
    clear_readonly_fields,
)


def clean(data: Dict) -> Dict:
    for i in clean_steps:
        data = i(data)
    return data


class ModelBiz:
    model: db.BaseModel = None
    model_schema: Type[BaseModel] = None

    def __init_subclass__(cls, **kwargs):
        assert cls.model is not None, f"{cls.__name__} can not be None"
        if cls.model_schema is None:
            cls.model_schema = model_to_schema(cls.model, exclude=list(ALWAYS_EXCLUDE))

    def create(self, create: BaseModel) -> db.BaseModel:
        create_data = clean(create.dict(exclude_unset=True))
        model = self.model(**create_data)
        db.session.add(model)
        db.session.commit()
        return model

    def delete(self, {{cookiecutter.business_key}}: str) -> None:
        model = self.retrieve({{cookiecutter.business_key}})
        db.session.delete(model)
        db.session.commit()

    def patch(self, {{cookiecutter.business_key}}: str, patch: BaseModel) -> db.BaseModel:
        model = self.retrieve({{cookiecutter.business_key}})
        patch_data = clean(patch.dict(exclude_unset=True))
        for k, v in patch_data.items():
            setattr(model, k, v)
        db.session.add(model)
        db.session.commit()
        db.session.refresh(model)
        return model

    def retrieve(self, {{cookiecutter.business_key}}: str) -> db.BaseModel:
        return db.session.query(self.model).filter(self.model.{{cookiecutter.business_key}} == {{cookiecutter.business_key}}).one()

    def _filtered_query(self, filters: BaseModel):
        q = db.session.query(self.model)
        for k, v in clean(filters.dict(exclude_defaults=True)).items():
            op, col_name = dj_lookup_to_sqla(k)
            q = q.filter(op(getattr(self.model, col_name), v))

        return q

    def bulk_retrieve(self, filters: BaseModel):
        q = self._filtered_query(filters)

        ordering = getattr(filters, "ordering", None)
        if ordering is not None:
            q = q.order_by(*map(dj_ordering_to_sqla, ordering))

        limit = getattr(filters, "limit", math.inf)
        if limit and not math.isinf(limit):
            q = q.limit(limit)

        offset = getattr(filters, "offset", 0)
        if offset:
            q = q.offset(offset)

        return q

    def count(self, filters: BaseModel) -> int:
        return int(
            self._filtered_query(filters)
            .with_entities(func.count(self.model.id))
            .scalar()
            or 0
        )

    def bulk_create(self, create: BulkCreateRequest) -> List[db.BaseModel]:
        objs = [self.model(**self.model_schema(**i).dict()) for i in create.data]
        if not objs:
            return []

        try:
            db.session.bulk_save_objects(objs)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
        else:
            return objs


from pytest_factoryboy import register
from apps.common.models import Language, PromoTypes, StatusMaster
import factory
import pandas as pd
import pandas as pd
from core.generics.respository import AbstractRepository
from core.generics.unit_of_work import AbstractUnitOfWork

language_data = {
    "language_id": 1,
    "language_code": "en",
    "language_description": "English",
    "currency_symbol": "$",
    "default_language": "1",
    "created_by": "manoj",
    "created_at": "2021-10-27T20:11:55.586456Z",
    "modified_by": "manoj",
    "modified_at": "2021-12-30T07:39:45.789439Z",
    "active": True,
}
status_data = {
    "id": 1,
    "status_name": "Saved",
    "status_code": 100,
    "created_by": "1",
    "created_at": "2021-11-13T14:14:00Z",
    "modified_by": "1",
    "modified_at": "2021-11-13T14:14:00Z",
    "active": True,
}
promo_types_data = {
    "promo_type_id": 1,
    "promo_type_name": "Individual",
    "promo_type_code": "ind",
    "active": True,
    "created_by": "admin",
    "created_at": "2021-12-01T14:30:32Z",
    "modified_by": None,
    "modified_at": "2021-12-01T14:30:32Z",
}


@register
class LanguageFactory(factory.Factory):
    language_id = 1
    language_code = "en"
    language_description = "English"
    currency_symbol = "$"
    default_language = "1"
    created_by = "manoj"
    created_at = factory.Faker("date")
    modified_by = "manoj"
    modified_at = factory.Faker("date")
    active = True

    class Meta:
        model = Language


@register
class PromoTypesFactory(factory.Factory):
    promo_type_id = 1
    promo_type_name = "Individual"
    promo_type_code = "ind"
    active = True
    created_by = "admin"
    created_at = factory.Faker("date")
    modified_by = "admin"
    modified_at = factory.Faker("date")

    class Meta:
        model = PromoTypes


@register
class StatusMasterFactory(factory.Factory):
    id = 1
    status_name = "Saved"
    status_code = 100
    created_by = ("manoj",)
    created_at = "2021-11-13T14:14:00Z"
    modified_by = "manoj"
    modified_at = "2021-11-13T14:14:00Z"
    active = True

    class Meta:
        model = StatusMaster


class FakeModel:
    def __init__(self, model):
        super().__init__([])
        self._model = dict(model)
        super().__init__([])

    def add(self, entity):
        self._model[entity[0]] = entity[1:]

    def delete(self, id):
        self._model.pop(id)

    def get(self, id=0):
        return [id] + self._model.get(id, [])

    def update(self, entity):
        self._model.update({entity[0]: entity[1:]})


class FakeRepository(AbstractRepository):
    def __init__(self, model):
        super().__init__([])
        self._model = dict(model)
        super().__init__([])

    def add(self, entity):
        self._model[entity[0]] = entity[1:]

    def delete(self, id):
        self._model.pop(id)

    def get(self, id=0):
        return [id] + self._model.get(id, [])

    def getAll(self, active=True):
        return [0] + self._model.get(0, [])

    def update(self, entity):
        self._model.update({entity[0]: entity[1:]})


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.model = FakeRepository([])
        self.repoObj = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        return True

    def add(self, entity):
        self.model.add(entity)

    def get_data_dict(self):
        return self.model.get()

    def get_data_df(self, query_string, sql_params):
        if sql_params[0] == "0":
            return pd.DataFrame(data=[])
        return pd.DataFrame(data=language_data, index=language_data.keys())

    def filter_by_metric_name(self, metric_names=[]):
        if metric_names:
            return [
                [i[0]] + list(i[1])
                for i in self.model._model.items()
                if i[1][0] in metric_names
            ]
        else:
            return list(self.model._model.items())

import pandas as pd
from apps.common.repository import (ItemRepository, LanguageRepository,
                                    PromoTypesRepository)
from core.generics.unit_of_work import ORMModelUnitOfWork
from django.db.models import Max


class LanguagesUnitOfWork(ORMModelUnitOfWork):
    def __init__(self, trans):
        super(LanguagesUnitOfWork, self).__init__(trans, LanguageRepository)

    def raw_queryset_as_values_list(self, raw_qs):
        columns = raw_qs.columns
        for row in raw_qs:
            yield tuple(getattr(row, col) for col in columns)

    def get_data_df(self, query_string, params):
        results = self.repoObj._model.raw(query_string, params)
        return pd.DataFrame(
            self.raw_queryset_as_values_list(results), columns=list(results.columns)
        )

    def get_raw_query_data(self, query_string, params):
        # return data as list of dicts
        results = self.repoObj._model.raw(query_string, params)
        columns = results.columns
        return [
            dict(tuple((col, getattr(row, col)) for col in columns)) for row in results
        ]

    def filter_by_language_code(self, language_codes=()):
        return self.repoObj._model.filter(language_code__in=language_codes)


class PromoTypesUnitOfWork(ORMModelUnitOfWork):
    def __init__(self, trans):
        super(PromoTypesUnitOfWork, self).__init__(trans, PromoTypesRepository)

class ItemsUnitOfWork(ORMModelUnitOfWork):
    def __init__(self, trans):
        super(ItemsUnitOfWork, self).__init__(trans, ItemRepository)

    def raw_queryset_as_values_list(self, raw_qs):
        columns = raw_qs.columns
        for row in raw_qs:
            yield tuple(getattr(row, col) for col in columns)

    def get_data_df(self, query_string, params):
        results = self.repoObj._model.raw(query_string, params)
        return pd.DataFrame(
            self.raw_queryset_as_values_list(results), columns=list(results.columns)
        )

    def get_raw_query_data(self, query_string, params):
        # return data as list of dicts
        results = self.repoObj._model.raw(query_string, params)
        columns = results.columns
        return [
            dict(tuple((col, getattr(row, col)) for col in columns)) for row in results
        ]

    def filter_by_item_code(self, item_codes=()):
        return self.repoObj._model.filter(item_code__in=item_codes)
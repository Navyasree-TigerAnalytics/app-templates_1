from apps.common.models import Item, Language, PromoTypes
from core.generics.respository import ORMModelRepository
from rest_framework.serializers import ValidationError


class LanguageRepository(ORMModelRepository):
    def __init__(self):
        super(LanguageRepository, self).__init__(Language)

    def get(self, uid):
        return self._model.filter(language_id=uid).first()

    def update(self, uid, entity):
        if self._model.filter(language_id=uid, active=True).first():
            self._model.filter(language_id=uid).update(**entity)
        else:
            raise ValidationError("cannot update inactive records")

    def delete(self, uid):
        if self._model.filter(language_id=uid, active=True).first():
            self._model.filter(language_id=uid).delete()
        else:
            raise ValidationError("cannot delete inactive records")


class PromoTypesRepository(ORMModelRepository):
    def __init__(self):
        super(PromoTypesRepository, self).__init__(PromoTypes)

class ItemRepository(ORMModelRepository):
    def __init__(self):
        super(ItemRepository, self).__init__(Item)

    def get(self, uid):
        return self._model.filter(item_id=uid).first()

    def update(self, uid, entity):
        if self._model.filter(item_id=uid, active=True).first():
            self._model.filter(item_id=uid).update(**entity)
        else:
            raise ValidationError("cannot update inactive records")

    def delete(self, uid):
        if self._model.filter(item_id=uid, active=True).first():
            self._model.filter(item_id=uid).delete()
        else:
            raise ValidationError("cannot delete inactive records")
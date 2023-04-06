from django.core.management import call_command
import factory
from pytest_factoryboy import register
import pytest
import os
import sys
from pathlib import Path
from apps.common import models, repository
from apps.common.tests import factories

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

sys.path.append(BASE_DIR.__str__())


@pytest.fixture(scope="module")
def django_db_setup():
    from django.conf import settings

    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(os.path.join(BASE_DIR, "mcdapi"), "testdb.sqlite3"),
    }


# this fixture is used to temporarily create data in the model for testing


@pytest.fixture(scope="session")
def django_data_setup(django_db_blocker):
    print("setup")

    with django_db_blocker.unblock():
        languages_repo = repository.LanguageRepository()
        languages_repo.add(factories.language_data)
        status_repo = repository.StatusMasterRepository()
        status_repo.add(factories.status_data)
        promo_types_repo = repository.PromoTypesRepository()
        promo_types_repo.add(factories.promo_types_data)

        model_obj_1 = models.Language(factories.LanguageFactory)
        model_obj_1.save()
        model_obj_2 = models.StatusMaster(factories.StatusMasterFactory)
        model_obj_2.save()
        model_obj_3 = models.PromoTypes(factories.PromoTypesFactory)
        model_obj_3.save()


register(
    factories.LanguageFactory,
    "language1",
    language_id=2,
    language_code="fr",
    language_description="French",
    currency_symbol="$$",
    default_language="1",
    created_by="manoj",
    created_at=factory.Faker("date"),
    modified_by="manoj",
    modified_at=factory.Faker("date"),
    active=True,
)

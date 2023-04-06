from django.apps import apps
from faker import Factory
from apps.common.tests.factories import FakeRepository
import pytest
from apps.common.unit_of_work import LanguagesUnitOfWork
import factory


@pytest.mark.django_db
def test_languages():
    unit_of_work = LanguagesUnitOfWork(factory.Faker("set_autocommit"))
    unit_of_work.smkpis_model = FakeRepository(
        [
            ("language_id", 1),
        ]
    )
    assert len(unit_of_work.repoObj.getAll(active=True)) > 1

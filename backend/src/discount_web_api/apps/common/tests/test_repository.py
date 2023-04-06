from django.apps import apps
from apps.common.tests.factories import LanguageFactory
import pytest
from apps.common.repository import LanguageRepository


@pytest.mark.django_db
def test_language_repo(language1):
    smkr = LanguageRepository()
    assert smkr.get(id=0) is None
    assert smkr.get(id=1) is not None
    assert language1.language_id == 2

from apps.common import models
from apps.common.tests.conftest import django_data_setup
import pytest


@pytest.mark.django_db
def test_create_language(django_data_setup):
    assert set(u.language_id for u in models.Language.objects.all()) == {1, None}


@pytest.mark.django_db
def test_statusmaster(django_data_setup):
    assert set(u.id for u in models.StatusMaster.objects.all()) == {1, None}


@pytest.mark.django_db
def test_promo_types(django_data_setup):
    assert set(u.promo_type_id for u in models.PromoTypes.objects.all()) == {1, None}

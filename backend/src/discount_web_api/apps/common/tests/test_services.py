from django.apps import apps
import pytest
from apps.common import services
from core.generics.exceptions import MissingRequestParamsError, NoDataError
from factories import FakeUnitOfWork

# Build paths inside the project like this: BASE_DIR / 'subdir'.


@pytest.mark.parametrize("value, expected", [("all", [0]), (1, [1])])
def test_get_languages(value, expected):
    uow = FakeUnitOfWork()
    uow.add([1, "en", "English", "$", "1", True, 1])
    assert services.get_languages(uow, value) == expected

    assert services.get_languages(uow, value) is not None

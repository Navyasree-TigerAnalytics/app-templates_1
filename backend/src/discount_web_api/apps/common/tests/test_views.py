import json
from sentry_sdk import Scope
import pytest
from rest_framework.test import APIClient

apiclient = APIClient()


@pytest.mark.django_db(transaction=True)
def test_get_languages(django_data_setup, django_db_setup):
    data_resp = apiclient.get("/api/v1/common/languages", format="json")
    assert data_resp.status_code == 200
    assert json.loads(data_resp.content)["data"] is not None
    assert json.loads(data_resp.content)["data"][0]["language_code"] == "en"

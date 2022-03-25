import pytest
from http import HTTPStatus

from arrival_test.alaska_api.alaska_api_utils import BearApiClient
from arrival_test.alaska_api.urls import BEAR_URL
from arrival_test.utils.logger import Logger as logger
from arrival_test.models.bear import Bear
from arrival_test.tests.checks import check_for_equality
from arrival_test.tests.test_data.constants import DEFAULT_BEAR_NAME, DEFAULT_BEAR_TYPE, DEFAULT_BEAR_AGE


@pytest.fixture(scope="session")
def setup_alaska_api():
    alaska_api = BearApiClient(BEAR_URL)
    yield alaska_api


@pytest.fixture(scope="session", autouse=True)
def check_application_status(setup_alaska_api):
    try:
        logger.info("Checking if application is running")
        status_code, bears_from_db = setup_alaska_api.get_all_bears()
    except WindowsError:
        pytest.exit('Application was not started!')
    else:
        yield


@pytest.fixture()
def empty_data_base(setup_alaska_api):
    setup_alaska_api.delete_all_bears()


@pytest.fixture()
def create_default_bear(setup_alaska_api):
    bear_data = Bear(bear_type=DEFAULT_BEAR_TYPE, bear_name=DEFAULT_BEAR_NAME, bear_age=DEFAULT_BEAR_AGE)
    resp_status_code, created_bear_id = setup_alaska_api.create_bear(bear_data)

    check_for_equality(resp_status_code, HTTPStatus.OK)
    bear_data.id = int(created_bear_id)
    return bear_data


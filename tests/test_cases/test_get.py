import pytest
from http import HTTPStatus
from arrival_test.alaska_api.alaska_api_utils import AlaskaApiUtils
from arrival_test.alaska_api.api_constants import NON_EXISTING_RECORD
from arrival_test.tests.checks import check_status_code, check_bear_data, check_bear_in_bears_list, check_for_equality
from arrival_test.models.bear import BearsGroup
from arrival_test.test_data.constants import DEFAULT_VALID_BEAR


@pytest.fixture()
def empty_data_base():
    AlaskaApiUtils.delete_all_bears()


class TestGet:

    def test_get_empty_db(self, empty_data_base):
        resp_status_code, resp_data = AlaskaApiUtils.get_all_bears()

        check_status_code(resp_status_code, HTTPStatus.OK)

        check_bear_data(resp_data, BearsGroup({}))

    def test_get_not_empty_db(self):
        bear_data = DEFAULT_VALID_BEAR
        resp_status_code, created_bear_id = AlaskaApiUtils.create_bear(bear_data.json_repr())

        check_status_code(resp_status_code, HTTPStatus.OK)

        bear_data.id = int(created_bear_id)

        resp_status_code, bears_data = AlaskaApiUtils.get_all_bears()

        check_status_code(resp_status_code, HTTPStatus.OK)

        check_bear_in_bears_list(bear_data, bears_data)

    def test_get_existing_id(self):
        bear_data = DEFAULT_VALID_BEAR
        resp_status_code, created_bear_id = AlaskaApiUtils.create_bear(bear_data.json_repr())

        check_status_code(resp_status_code, HTTPStatus.OK)

        bear_data.id = int(created_bear_id)

        resp_status_code, bear_data_from_db = AlaskaApiUtils.get_bear_by_id(created_bear_id)
        check_status_code(resp_status_code, HTTPStatus.OK)

        check_bear_data(bear_data_from_db, bear_data)

    def test_get_non_existing_id(self):
        bear_data = DEFAULT_VALID_BEAR
        resp_status_code, created_bear_id = AlaskaApiUtils.create_bear(bear_data.json_repr())

        non_existing_id = int(created_bear_id) + 1

        check_status_code(resp_status_code, HTTPStatus.OK)

        resp_status_code, resp_data = AlaskaApiUtils.get_bear_by_id(non_existing_id)
        check_status_code(resp_status_code, HTTPStatus.OK)

        check_for_equality(resp_data, NON_EXISTING_RECORD)
        


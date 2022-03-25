import pytest
from http import HTTPStatus
from arrival_test.alaska_api.constants import NON_EXISTING_RECORD
from arrival_test.tests.checks import check_for_equality, check_bear_data, check_bear_in_bears_list
from arrival_test.models.bear import BearsGroup


class TestGet:

    def test_get_empty_db(self, setup_alaska_api, empty_data_base):
        resp_status_code, bears_from_db = setup_alaska_api.get_all_bears()
        check_for_equality(resp_status_code, HTTPStatus.OK)
        check_bear_data(bears_from_db, BearsGroup({}))

    @pytest.mark.xfail
    def test_get_not_empty_db(self, setup_alaska_api, create_default_bear):
        resp_status_code, bears_from_db = setup_alaska_api.get_all_bears()
        check_for_equality(resp_status_code, HTTPStatus.OK)
        check_bear_in_bears_list(create_default_bear, bears_from_db)

    @pytest.mark.xfail
    def test_get_existing_id(self, setup_alaska_api, create_default_bear):
        resp_status_code, bear_from_db = setup_alaska_api.get_bear_by_id(create_default_bear.id)
        check_for_equality(resp_status_code, HTTPStatus.OK)
        check_bear_data(bear_from_db, create_default_bear)

    def test_get_non_existing_id(self, setup_alaska_api, create_default_bear):
        non_existing_id = create_default_bear.id + 1
        resp_status_code, bear_from_db = setup_alaska_api.get_bear_by_id(non_existing_id)
        check_for_equality(resp_status_code, HTTPStatus.OK)
        check_for_equality(bear_from_db, NON_EXISTING_RECORD)

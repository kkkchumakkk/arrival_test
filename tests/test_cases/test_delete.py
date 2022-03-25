import pytest
from http import HTTPStatus
from arrival_test.alaska_api.constants import SUCCESSFUL_UPDATE
from arrival_test.models.bear import BearsGroup
from arrival_test.tests.checks import check_for_equality, check_bear_in_bears_list


class TestDelete:

    def test_delete_with_valid_id(self, setup_alaska_api, create_default_bear):
        resp_status_code, delete_result = setup_alaska_api.delete_bear_by_id(create_default_bear.id)
        check_for_equality(resp_status_code, HTTPStatus.OK)
        check_for_equality(delete_result, SUCCESSFUL_UPDATE)

        resp_status_code, bears = setup_alaska_api.get_all_bears()
        check_bear_in_bears_list(create_default_bear, bears, False)

    @pytest.mark.xfail
    def test_delete_with_not_valid_id(self, setup_alaska_api, create_default_bear):
        resp_status_code, bears_from_db_before = setup_alaska_api.get_all_bears()

        resp_status_code, delete_result = setup_alaska_api.delete_bear_by_id(create_default_bear.id+1)
        check_for_equality(resp_status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

        resp_status_code, bears_from_db_after = setup_alaska_api.get_all_bears()
        check_for_equality(bears_from_db_before, bears_from_db_after)

    @pytest.mark.xfail
    def test_delete_double_delete_for_record(self, setup_alaska_api, create_default_bear):
        resp_status_code, delete_result = setup_alaska_api.delete_bear_by_id(create_default_bear.id)
        check_for_equality(resp_status_code, HTTPStatus.OK)
        check_for_equality(delete_result, SUCCESSFUL_UPDATE)

        resp_status_code, bear_from_db = setup_alaska_api.get_all_bears()
        check_bear_in_bears_list(create_default_bear, bear_from_db, False)

        resp_status_code, delete_result = setup_alaska_api.delete_bear_by_id(create_default_bear.id)
        check_for_equality(resp_status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_delete_all_records(self, setup_alaska_api):
        resp_status_code, delete_result = setup_alaska_api.delete_all_bears()
        check_for_equality(resp_status_code, HTTPStatus.OK)
        check_for_equality(delete_result, BearsGroup({}))

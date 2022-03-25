import pytest
from http import HTTPStatus
from arrival_test.alaska_api.constants import ERROR_MSG_PLEASE_FILL_ALL_THE_PARAMS, FIELD_BEAR_TYPE
from arrival_test.tests.steps import generate_bear
from arrival_test.tests.common_steps import generate_and_check_bear
from arrival_test.tests.checks import check_for_equality, check_bear_data, check_bear_in_bears_list
from arrival_test.models.bear import Bear
from arrival_test.tests.test_data.constants import INCORRECT_BEAR_TYPE, INCORRECT_BEAR_NAME, INCORRECT_BEAR_AGE, \
    EMPTY_BEAR_DATA


class TestPost:

    @pytest.mark.xfail
    @pytest.mark.parametrize('bear_type', [Bear.BEAR_TYPE_POLAR, Bear.BEAR_TYPE_BLACK, Bear.BEAR_TYPE_BROWN,
                                           pytest.param(Bear.BEAR_TYPE_GUMMY,
                                                        marks=pytest.mark.xfail(raises=AttributeError))])
    def test_post_for_bear_type(self, setup_alaska_api, bear_type):
        generated_bear = generate_and_check_bear(setup_alaska_api, {FIELD_BEAR_TYPE: bear_type})

        resp_status_code, bear_from_db = setup_alaska_api.get_bear_by_id(generated_bear.id)
        check_for_equality(resp_status_code, HTTPStatus.OK)
        check_bear_data(bear_from_db, generated_bear)

    @pytest.mark.parametrize('bear_with_invalid_data',
                             [pytest.param(generate_bear(bear_type=INCORRECT_BEAR_TYPE), id="Invalid bear type"),
                              pytest.param(generate_bear(bear_name=INCORRECT_BEAR_NAME), id="Invalid bear name"),
                              pytest.param(generate_bear(bear_age=INCORRECT_BEAR_AGE), id="Invalid bear age"),
                              pytest.param(generate_bear(**EMPTY_BEAR_DATA), id="Empty fields")])
    def test_post_with_invalid_data(self, setup_alaska_api, bear_with_invalid_data):
        resp_status_code, created_bear_id = setup_alaska_api.create_bear(bear_with_invalid_data)
        check_for_equality(resp_status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

        resp_status_code, bears_from_db = setup_alaska_api.get_all_bears()
        check_bear_in_bears_list(bear_with_invalid_data, bears_from_db, False)

    def test_post_with_empty_body(self, setup_alaska_api):
        resp_status_code, bears_from_db_before = setup_alaska_api.get_all_bears()

        resp_status_code, err_msg = setup_alaska_api.create_bear()
        check_for_equality(resp_status_code, HTTPStatus.OK)
        check_for_equality(err_msg, ERROR_MSG_PLEASE_FILL_ALL_THE_PARAMS)

        resp_status_code, bears_from_db_after = setup_alaska_api.get_all_bears()
        check_for_equality(bears_from_db_before, bears_from_db_after)

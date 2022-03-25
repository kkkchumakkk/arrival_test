import pytest
from http import HTTPStatus
from arrival_test.alaska_api.alaska_api_utils import AlaskaApiUtils
from arrival_test.alaska_api.api_constants import ERROR_MSG_PLEASE_FILL_ALL_THE_PARAMS
from arrival_test.tests.steps import generate_bear
from arrival_test.tests.checks import check_status_code, check_bear_data, check_bear_in_bears_list, check_error_msg, \
    check_bears_data_for_equality
from arrival_test.models.bear import Bear
from arrival_test.test_data.constants import INCORRECT_BEAR_TYPE, INCORRECT_BEAR_NAME, INCORRECT_BEAR_AGE, \
    EMPTY_BEAR_DATA


class TestPost:

    @pytest.mark.parametrize('bear_type', [Bear.BEAR_TYPE_POLAR, Bear.BEAR_TYPE_BLACK, Bear.BEAR_TYPE_BROWN,
                                           pytest.param(Bear.BEAR_TYPE_GUMMY,
                                                        marks=pytest.mark.xfail(raises=AttributeError))])
    def test_post_for_bear_type(self, bear_type):
        generated_bear = generate_bear(bear_type=bear_type)

        resp_status_code, created_bear_id = AlaskaApiUtils.create_bear(generated_bear.json_repr())

        check_status_code(resp_status_code, HTTPStatus.OK)
        generated_bear.id = int(created_bear_id)

        resp_status_code, bear_from_db = AlaskaApiUtils.get_bear_by_id(created_bear_id)
        check_status_code(resp_status_code, HTTPStatus.OK)
        check_bear_data(bear_from_db, generated_bear)

    @pytest.mark.parametrize('bear_with_invalid_data',
                             [pytest.param(generate_bear(bear_type=INCORRECT_BEAR_TYPE), id="Invalid bear type"),
                              pytest.param(generate_bear(bear_name=INCORRECT_BEAR_NAME), id="Invalid bear name"),
                              pytest.param(generate_bear(bear_age=INCORRECT_BEAR_AGE), id="Invalid bear age"),
                              pytest.param(generate_bear(**EMPTY_BEAR_DATA), id="Empty fields")])
    def test_post_with_invalid_data(self, bear_with_invalid_data):
        resp_status_code, _ = AlaskaApiUtils.create_bear(bear_with_invalid_data.json_repr())

        check_status_code(resp_status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

        resp_status_code, bear_data = AlaskaApiUtils.get_all_bears()

        check_bear_in_bears_list(bear_with_invalid_data, bear_data, False)

    def test_post_with_empty_body(self):
        _, bears_data_before = AlaskaApiUtils.get_all_bears()

        resp_status_code, err_msg = AlaskaApiUtils.create_bear()

        check_status_code(resp_status_code, HTTPStatus.OK)

        check_error_msg(err_msg, ERROR_MSG_PLEASE_FILL_ALL_THE_PARAMS)

        _, bears_data_after = AlaskaApiUtils.get_all_bears()

        check_bears_data_for_equality(bears_data_before, bears_data_after)



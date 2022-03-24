import pytest
from http import HTTPStatus
from arrival_test.utils.alaska_api_utils import AlaskaApiUtils
from arrival_test.utils.utilities import soft_assert
from arrival_test.utils.random_utils import RandomUtils
from arrival_test.utils.logger import Logger
from arrival_test.test_data.constants import Constants


class TestPost:

    @pytest.mark.parametrize('bear_type', [Constants.BEAR_TYPE_POLAR, Constants.BEAR_TYPE_BLACK,
                                           Constants.BEAR_TYPE_BROWN,
                                           pytest.param(Constants.BEAR_TYPE_GUMMY,
                                                        marks=pytest.mark.xfail(raises=TypeError))])
    def test_post_for_bear_type(self, bear_type):
        Logger.info(f'Starting test for method "POST" for bear type {bear_type}.')
        bear_name = RandomUtils.gen_random_string(Constants.DEFAULT_STRING_LENGTH)
        bear_age = RandomUtils.gen_random_float(*Constants.BEAR_AGE_INTERVAL)
        bear_data = dict(zip([Constants.FIELD_BEAR_TYPE, Constants.FIELD_BEAR_NAME, Constants.FIELD_BEAR_AGE],
                             [bear_type, bear_name, bear_age]))

        resp_status_code, created_bear_id = AlaskaApiUtils.create_bear(bear_data)

        assert resp_status_code == HTTPStatus.OK, f'Status code for response does not match with expected. ' \
                                                  f'Expected: {HTTPStatus.OK}. ' \
                                                  f'Actual: {resp_status_code}'

        bear_data.update({Constants.FILED_BEAR_ID: int(created_bear_id)})

        resp_status_code, resp_data = AlaskaApiUtils.get_bear_by_id(created_bear_id)
        assert resp_status_code == HTTPStatus.OK, f'Status code for response does not match with expected. ' \
                                                  f'Expected: {HTTPStatus.OK}. ' \
                                                  f'Actual: {resp_status_code}'
        soft_assert(resp_data, bear_data)
        Logger.info(f'Test for method "POST" for bear type {bear_type} ended.')

    @pytest.mark.parametrize('bear_type,bear_name,bear_age',
                             [
                                 pytest.param(RandomUtils.gen_random_string(Constants.DEFAULT_STRING_LENGTH),
                                              RandomUtils.gen_random_string(Constants.DEFAULT_STRING_LENGTH),
                                              RandomUtils.gen_random_float(*Constants.BEAR_AGE_INTERVAL),
                                              id="Invalid bear type"),
                                 pytest.param(RandomUtils.gen_random_from_set(Constants.AVAILABLE_BEAR_TYPES),
                                              Constants.INVALID_BEAR_NAME,
                                              RandomUtils.gen_random_float(*Constants.BEAR_AGE_INTERVAL),
                                              id="Invalid bear name"),
                                 pytest.param(RandomUtils.gen_random_from_set(Constants.AVAILABLE_BEAR_TYPES),
                                              RandomUtils.gen_random_string(Constants.DEFAULT_STRING_LENGTH),
                                              RandomUtils.gen_random_string(Constants.DEFAULT_STRING_LENGTH),
                                              id="Invalid bear age"),
                                 pytest.param("", "", "", id="Empty fields")])
    def test_post_with_invalid_data(self, bear_type, bear_name, bear_age):
        Logger.info(f'Starting test for method "POST" with bear data {bear_type, bear_name, bear_age}')
        bear_data = dict(zip([Constants.FIELD_BEAR_TYPE, Constants.FIELD_BEAR_NAME, Constants.FIELD_BEAR_AGE],
                             [bear_type, bear_name, bear_age]))

        resp_status_code, created_bear_id = AlaskaApiUtils.create_bear(bear_data)

        assert resp_status_code == HTTPStatus.INTERNAL_SERVER_ERROR, \
            f'Status code for response does not match with expected. ' \
            f'Expected: {HTTPStatus.INTERNAL_SERVER_ERROR}. ' \
            f'Actual: {resp_status_code}'
        Logger.info(f'"Test for method "POST" with invalid data ended.')

    def test_post_with_empty_body(self):
        Logger.info(f'"Starting test for method "Post" with empty body')
        resp_status_code, resp_data = AlaskaApiUtils.create_bear()
        assert resp_status_code == HTTPStatus.OK, f'Status code for response does not match with expected. ' \
                                                  f'Expected: {HTTPStatus.OK}. ' \
                                                  f'Actual: {resp_status_code}'
        assert resp_data == Constants.ERROR_MSG_PLEASE_FILL_ALL_THE_PARAMS, \
            f'Response body does not match with expected. ' \
            f'Expected {Constants.ERROR_MSG_PLEASE_FILL_ALL_THE_PARAMS}.' \
            f'Actual: {Constants.ERROR_MSG_PLEASE_FILL_ALL_THE_PARAMS}'
        Logger.info(f'"Test for method "POST" with empty body')


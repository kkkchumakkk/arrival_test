import pytest
import random
import string
from http import HTTPStatus
from arrival_test.alaska_api.constants import ERROR_MSG_PLEASE_FILL_ALL_THE_PARAMS, \
    FIELD_BEAR_AGE, FIELD_BEAR_NAME, FIELD_BEAR_TYPE
from arrival_test.tests.steps import generate_bear
from arrival_test.tests.common_steps import generate_and_check_bear, update_with_valid_data_and_check
from arrival_test.tests.checks import check_for_equality, check_bear_data
from arrival_test.models.bear import Bear
from arrival_test.tests.test_data.constants import EMPTY_BEAR_DATA


class TestPut:

    @pytest.mark.xfail
    @pytest.mark.parametrize('initial_bear_type, new_bear_type',
                             [(Bear.BEAR_TYPE_POLAR, Bear.BEAR_TYPE_BROWN),
                              (Bear.BEAR_TYPE_BLACK, Bear.BEAR_TYPE_POLAR),
                              (Bear.BEAR_TYPE_BROWN, Bear.BEAR_TYPE_GUMMY),
                              (Bear.BEAR_TYPE_GUMMY, Bear.BEAR_TYPE_BLACK)])
    def test_put_for_valid_bear_type(self, setup_alaska_api, initial_bear_type, new_bear_type):
        generated_bear = generate_and_check_bear(setup_alaska_api, {FIELD_BEAR_TYPE: initial_bear_type})
        generated_bear.type = new_bear_type

        update_with_valid_data_and_check(setup_alaska_api, generated_bear)

    @pytest.mark.parametrize('initial_bear_name, new_bear_name',
                             [(''.join(random.choices(string.ascii_letters, k=Bear.DEFAULT_BEAR_NAME_LENGTH)),
                               ''.join(random.choices(string.ascii_letters, k=Bear.DEFAULT_BEAR_NAME_LENGTH)))])
    def test_put_for_valid_bear_name(self, setup_alaska_api, initial_bear_name, new_bear_name):
        generated_bear = generate_and_check_bear(setup_alaska_api, {FIELD_BEAR_NAME: initial_bear_name})
        generated_bear.name = new_bear_name

        update_with_valid_data_and_check(setup_alaska_api, generated_bear)

    @pytest.mark.xfail
    @pytest.mark.parametrize('initial_bear_age, new_bear_age',
                             [(round(random.uniform(*Bear.ALLOWED_BEAR_AGE_INTERVAL), Bear.DEFAULT_AGE_PRECISION),
                               round(random.uniform(*Bear.ALLOWED_BEAR_AGE_INTERVAL), Bear.DEFAULT_AGE_PRECISION))])
    def test_put_for_valid_bear_age(self, setup_alaska_api, initial_bear_age, new_bear_age):
        generated_bear = generate_and_check_bear(setup_alaska_api, {FIELD_BEAR_AGE: initial_bear_age})
        generated_bear.age = new_bear_age

        update_with_valid_data_and_check(setup_alaska_api, generated_bear)

    @pytest.mark.xfail
    def test_put_for_empty_body(self, setup_alaska_api):
        generated_bear = generate_bear()
        resp_status_code, created_bear_id = setup_alaska_api.create_bear(generated_bear)
        check_for_equality(resp_status_code, HTTPStatus.OK)
        generated_bear.id = int(created_bear_id)

        bear_with_empty_data = Bear(**EMPTY_BEAR_DATA)
        resp_status_code, err_msg = setup_alaska_api.update_bear_by_id(created_bear_id, bear_with_empty_data)
        check_for_equality(resp_status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        check_for_equality(err_msg, ERROR_MSG_PLEASE_FILL_ALL_THE_PARAMS)

        resp_status_code, bear_from_db = setup_alaska_api.get_bear_by_id(created_bear_id)
        check_for_equality(resp_status_code, HTTPStatus.OK)
        check_bear_data(generated_bear, bear_from_db)

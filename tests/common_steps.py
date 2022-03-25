from http import HTTPStatus
from arrival_test.tests.steps import generate_bear
from arrival_test.tests.checks import check_for_equality, check_bear_data
from arrival_test.alaska_api.constants import SUCCESSFUL_UPDATE


def generate_and_check_bear(setup_alaska_api, bear_data):
    generated_bear = generate_bear(**bear_data)
    resp_status_code, created_bear_id = setup_alaska_api.create_bear(generated_bear)
    check_for_equality(resp_status_code, HTTPStatus.OK)
    generated_bear.id = int(created_bear_id)

    return generated_bear


def update_with_valid_data_and_check(setup_alaska_api, new_bear):
    resp_status_code, message = setup_alaska_api.update_bear_by_id(new_bear.id, new_bear)
    check_for_equality(resp_status_code, HTTPStatus.OK)
    check_for_equality(message, SUCCESSFUL_UPDATE)

    resp_status_code, bear_data_from_db = setup_alaska_api.get_bear_by_id(new_bear.id)
    check_for_equality(resp_status_code, HTTPStatus.OK)
    check_bear_data(bear_data_from_db, new_bear)

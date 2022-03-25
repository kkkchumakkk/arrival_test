from arrival_test.utils.logger import Logger as logger


def check_for_equality(actual_result, expected_result):
    logger.info('Checking if actual result matches with expected.')
    assert actual_result == expected_result, "Actual result does not match with expected." \
                                             f"Expected: {expected_result}." \
                                             f"Actual: {actual_result}."


def check_status_code(actual_status_code, expected_status_code):
    logger.info(f'Checking status code')
    assert actual_status_code == expected_status_code, f'Status code for response does not match with expected. ' \
                                                       f'Expected: {expected_status_code}. ' \
                                                       f'Actual: {actual_status_code}'


def check_bear_data(actual_bear_data, expected_bear_data):
    logger.info(f'Checking bear')
    assert actual_bear_data == expected_bear_data, f'Bear data does not match with expected.' \
                                                   f'{actual_bear_data.get_diff(expected_bear_data)}'


def check_bear_in_bears_list(required_bear, list_of_bears, should_exist=True):
    logger.info(f'Checking if {required_bear} exists in DB')
    assert (required_bear in list_of_bears) == should_exist, f'Bear {required_bear} ' \
                                                             f'{"" if should_exist else "does not "} exists in DB. ' \
                                                             f'Bears in DB {list_of_bears}'


def check_error_msg(actual_err_msg, expected_err_msg):
    logger.info(f'Checking error message')
    assert actual_err_msg == expected_err_msg, \
        f'Error message does not match with expected. ' \
        f'Expected: {expected_err_msg}.' \
        f'Actual: {actual_err_msg}'


def check_bears_data_for_equality(actual_bears, expected_bears):
    logger.info(f'Checking if bears data matches with expected.')
    assert actual_bears == expected_bears, f'Bears data does not match with expected.' \
                                           f'Expected: {expected_bears}.' \
                                           f'Actual: {expected_bears}'

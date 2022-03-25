from arrival_test.utils.logger import Logger as logger


def check_for_equality(actual_result, expected_result):
    """
    Method to check actual result and expected result for equality

    @return: None

    @param actual_result: actual result that received in test
    @param expected_result: expected result to compare with actual result
    """
    logger.info('Checking if actual result matches with expected.')
    assert actual_result == expected_result, "Actual result does not match with expected." \
                                             f"Expected: {expected_result}." \
                                             f"Actual: {actual_result}."


def check_bear_data(actual_bear_data, expected_bear_data):
    """
    Method to check two bears instances for equality

    @return: None

    @param actual_bear_data: Bear instance that was received in test
    @param expected_bear_data: expected Bear instance to compare with actual result
    """
    logger.info(f'Checking bear')
    assert actual_bear_data == expected_bear_data, f'Bear data does not match with expected.' \
                                                   f'{actual_bear_data.get_diff(expected_bear_data)}'


def check_bear_in_bears_list(required_bear, list_of_bears, should_exist=True):
    """
    Method checks if Bear instance exists in BearGroup instance

    @return: None

    @param required_bear: Bear instance
    @param list_of_bears: Bear Group instance
    @param should_exist: True if Bear instance should exist in BearGroup instance, False otherwise
    """
    logger.info(f'Checking if {required_bear} exists in DB')
    assert (required_bear in list_of_bears) == should_exist, f'Bear {required_bear} ' \
                                                             f'{"" if should_exist else "does not "} exists in DB. ' \
                                                             f'Bears in DB {list_of_bears}'

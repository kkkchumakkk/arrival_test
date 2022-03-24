def get_dict_from_list_by_value(list_of_dicts, key_name, value):
    try:
        return [item for item in list_of_dicts if item[key_name] == value][0]
    except IndexError:
        raise AssertionError(f'There is no dict containing key {key_name} and value {value}')


def soft_assert(actual_result, expected_result):
    err_msg = ''
    for key in expected_result:
        try:
            assert actual_result[key] == expected_result[key]
        except AssertionError:
            err_msg += f'Value for {key} does not match with expected.' \
                       f'Expected: {expected_result[key]}.' \
                       f'Actual: {actual_result[key]}.'
        except KeyError:
            err_msg += f'Actual result does not contain field {key}.'
    assert not err_msg, err_msg

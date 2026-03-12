def to_bool(enabled_disabled: str) -> bool:
    """
    Converts the given string to a boolean value or raises a ValueError, if an unexpected value is supplied.
    :param enabled_disabled: 'Enabled' -> true; 'Disabled' -> false
    :return: the converted boolean value
    """
    if enabled_disabled == 'Enabled':
        return True
    elif enabled_disabled == 'Disabled':
        return False
    else:
        raise ValueError(f'Argument \'enabled_disabled\' has an unexpected value! Expected either \'Enabled\' or'
                         f' \'Disabled\', but was \'{enabled_disabled}\'!')


def to_hex_str(int_value):
    return format(int_value, 'x')

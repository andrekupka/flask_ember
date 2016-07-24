import warnings


def merge_dicts(source, target, warning_message=None):
    """ Merges entries from the source dict into the target dict. If a
    warning message is set and an entry from the target dict is overwritten
    the warning message is printed.

    :param source: The source dict to be merged from.
    :type source: dict
    :param target: The target dict to be merged into.
    :type target: dict
    :param warning_message: The warning message that is displayed if an entry
                            in the target dict is overwritten. It must contain
                            two format replacement fields where the entry's
                            name and new value can be inserted.
    :type warning_message: str
    """
    for name, value in source.items():
        if warning_message is not None and name in target:
            warnings.warn(warning_message.format(name, value))
        target[name] = value

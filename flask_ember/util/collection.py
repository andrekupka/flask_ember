def filter_dict_values(dictionary, predicate):
    """Filters the given dictionary by the given predicate and returns a new
    dictionary with the values that fulfill the predicate.

    :param dictionary: the dictionary to filter
    :type dictionary: dict
    :param predicate: the predicate
    :type predicate: function(key, value)
    :rtype: dict
    """
    return dict((key, value) for key, value in dictionary.items()
                if predicate(key, value))

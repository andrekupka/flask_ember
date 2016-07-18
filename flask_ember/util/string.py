import re

from .cached_function import CachedFunction


CAMELIZE_REGEXP_1 = re.compile(r'(\-|_|\.|\s)+(.)?')
CAMELIZE_REGEXP_2 = re.compile(r'(^|/)([A-Z])')


def do_camelize(s):
    s = CAMELIZE_REGEXP_1.sub(lambda m: m.group(2).upper(), s)
    s = CAMELIZE_REGEXP_2.sub(lambda m: m.group(0).lower(), s)
    return s


CAPITALIZE_REGEXP = re.compile(r'(^|/)([a-z])')


def do_capitalize(s):
    return CAPITALIZE_REGEXP.sub(lambda m: m.group(0).upper(), s)


CLASSIFY_REGEXP_1 = re.compile(r'^(\-|_)+(.)?')
CLASSIFY_REGEXP_2 = re.compile(r'(.)(\-|\_|\.|\s)+(.)?')
CLASSIFY_REGEXP_3 = re.compile(r'(^|/|\.)([a-z])')


def do_classify(s):
    def replace_part(part):
        part = CLASSIFY_REGEXP_1.sub(lambda m: '_' + m.group(2).upper(), part)
        return CLASSIFY_REGEXP_2.sub(lambda m: m.group(1) + m.group(3).upper(),
                                     part)

    parts = map(replace_part, s.split('/'))
    s = '/'.join(parts)
    return CLASSIFY_REGEXP_3.sub(lambda m: m.group(0).upper(), s)


DASHERIZE_REGEX = re.compile(r'[ _]')


def do_dasherize(s):
    return DASHERIZE_REGEX.sub('-', decamelize(s))


DECAMELIZE_REGEXP = re.compile(r'([a-z\d])([A-Z])')


def do_decamelize(s):
    return DECAMELIZE_REGEXP.sub(r'\1_\2', s).lower()


UNDERSCORE_REGEXP_1 = re.compile(r'([a-z\d])([A-Z]+)')
UNDERSCORE_REGEXP_2 = re.compile(r'\-|\s+')


def do_underscore(s):
    s = UNDERSCORE_REGEXP_1.sub(r'\1_\2', s)
    s = UNDERSCORE_REGEXP_2.sub('_', s)
    return s.lower()


camelize = CachedFunction(do_camelize)
capitalize = CachedFunction(do_capitalize)
classify = CachedFunction(do_classify)
dasherize = CachedFunction(do_dasherize)
decamelize = CachedFunction(do_decamelize)
underscore = CachedFunction(do_underscore)

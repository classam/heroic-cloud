import utils
import json
try:
    from google.appengine.ext import ndb
except ImportError:
    from stubs import ndb

PROPERTY_TYPES = {
    'string': ndb.StringProperty,
    'text': ndb.TextProperty,
    'boolean': ndb.BooleanProperty,
    'integer': ndb.IntegerProperty,
    'float': ndb.FloatProperty,
    'blob': ndb.BlobProperty,
    'datetime': ndb.DateTimeProperty,
    'date': ndb.DateProperty,
    'time': ndb.TimeProperty,
    'geopt': ndb.GeoPtProperty,
    'key': ndb.KeyProperty,
    'blobkey': ndb.BlobKeyProperty,
    'user': ndb.UserProperty,
    'structured': ndb.StructuredProperty,
    'localstructured': ndb.LocalStructuredProperty,
    'json': ndb.JsonProperty,
    'pickle': ndb.PickleProperty,
    'computed': ndb.ComputedProperty
}

# As we improve, this list will get less comprehensive
UNSUPPORTED = ['blob', 'computed', 'pickle', 'structured',
               'localstructured', 'geopt', 'user']

SUPPORTED = [x for x in PROPERTY_TYPES.keys() if x not in UNSUPPORTED]

SUPPORTS_COMPRESSED = ['localstructured', 'structured', 'json',
                       'pickle', 'blob']

OPTION_TYPES = ['indexed', 'repeated', 'required', 'default', 'compressed']


def generate_property(descriptor):
    assert(type(descriptor) == str)
    value, options = parse_option_format(descriptor)
    return get_google_property(value, options)


def parse_option_format(value):
    """
        Convert "string length|500 lower" into

        >>> parse_option_format("string default|awesome required")
        ('string', {'default': 'awesome', 'required': True})
        >>> parse_option_format("integer default|833")
        ('integer', {'default': '833'})
        >>> parse_option_format("datetime")
        ('datetime', {})

    """
    assert(type(value) == str)

    value_and_options = value.split(" ")
    if len(value_and_options) == 1:
        value = value_and_options[0]
        options = {}
    else:
        value = value_and_options[0]
        sets = value_and_options[1:]
        options = {}
        for st in sets:
            option = st.split("|")
            if len(option) == 1:
                options[option[0]] = True
            elif len(option) == 2:
                option_val = option[1]
                if option_val.lower() == "true":
                    option_val = True
                if option_val.lower() == "false":
                    option_val = False
                options[option[0]] = option[1]
            else:
                options[option[0]] = option[1:]
    return value, options


class InvalidPropertyType(Exception):
    pass


class CantParse(Exception):
    pass


def parse_by_type(property_class, parse_target):
    if property_class in [ndb.StringProperty, ndb.TextProperty]:
        if parse_target.lower() == "none":
            return ""
        else:
            return parse_target
    if property_class == ndb.KeyProperty:
        return parse_target
    if property_class == ndb.IntegerProperty:
        try:
            return int(parse_target)
        except ValueError:
            raise CantParse(parse_target + " is not an integer")
    if property_class == ndb.BooleanProperty:
        if parse_target.lower() in ["true", "t"]:
            return True
        elif parse_target.lower() in ["false", "f"]:
            return False
        else:
            raise CantParse(parse_target + " must be true or false")
    if property_class == ndb.FloatProperty:
        try:
            return float(parse_target)
        except ValueError:
            raise CantParse(parse_target + " is not a float")
    if property_class == ndb.JsonProperty:
        try:
            return json.loads(parse_target)
        except ValueError:
            raise CantParse(parse_target + " is not valid JSON")

    raise CantParse(property_class.__name__ + " can't be parsed")


def parse_by_string(string_, parse_target):
    """
        Given a string, parse into the type indicated by that string.

        >>> parse_by_string( "string", "hello world" )
        'hello world'
        >>> parse_by_string( "text", "hello world" )
        'hello world'
        >>> parse_by_string( "key", "Card:29s8312sa" )
        'Card:29s8312sa'
        >>> parse_by_string( "integer", "222" )
        222
        >>> parse_by_string( "integer", "garblepoop" )
        Traceback (most recent call last):
        ...
        CantParse: garblepoop is not an integer
        >>> parse_by_string( "boolean", "true" )
        True
        >>> parse_by_string( "boolean", "FALSE" )
        False
        >>> parse_by_string( "boolean", "garblepoop" )
        Traceback (most recent call last):
        ...
        CantParse: garblepoop must be true or false
        >>> parse_by_string( "float", "2.34" )
        2.34
        >>> parse_by_string( "float", "garblepoop" )
        Traceback (most recent call last):
        ...
        CantParse: garblepoop is not a float
        >>> parse_by_string( "blob", "anything" )
        Traceback (most recent call last):
        ...
        CantParse: blob type is currently not supported
        >>> parse_by_string( "dongs", "dongs" )
        Traceback (most recent call last):
        ...
        CantParse: dongs is not a valid type
    """
    if string_ in UNSUPPORTED:
        raise CantParse(string_ + " type is currently not supported")
    try:
        return parse_by_type(PROPERTY_TYPES[string_], parse_target)
    except KeyError:
        raise CantParse(string_ + " is not a valid type")


def get_google_property(type_string, options={}):
    if type_string not in SUPPORTED:
        raise InvalidPropertyType(string_ +
                                  " is not a supported property type.")

    options = utils.filter_keys(options, OPTION_TYPES)

    if 'default' in options:
        options['default'] = parse_by_string(type_string, options['default'])

    return PROPERTY_TYPES[type_string](**options)

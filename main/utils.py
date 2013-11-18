import inspect
"""
    Every project has a utils, right?
    Stuff you might want to do again and again.
"""


def filter_keys(dictionary, keys):
    """
    Delete any key-value pairs in the dictionary that aren't in keys.

    >>> filter_keys( {'a':1, 'b':2, 'c':3 }, ['a', 'b'] )
    {'a': 1, 'b': 2}

    """
    newdict = {}
    for key, value in dictionary.iteritems():
        if key in keys:
            newdict[key] = value
    return newdict


def asciify(target):
    """
    Convert something from u'blarg' to 'blarg'

    >>> asciify( u'potato' )
    'potato'
    >>> asciify( 'potato' )
    'potato'
    >>> asciify( {u'potato':u'thing'} )
    {'potato': 'thing'}
    >>> asciify( {u'potato':{u'potato':u'thing'}})
    {'potato': {'potato': 'thing'}}

    """
    if type(target) == unicode:
        return target.encode('ascii', 'ignore')
    elif type(target) == dict:
        return dict(map(asciify, pair) for pair in target.items())
    else:
        return target


def inspect_class(target):
    """
    Print everything you can about a class.
    """
    if not inspect.isclass(target):
        print target, " is not a class"
        return

    print target.__name__

    for member, value in inspect.getmembers(target):
        if member.startswith("__"):
            continue
        print "\t", member, "\t\t", value

    print "------------------"

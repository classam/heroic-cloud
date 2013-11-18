from entity_gen import generate_entity

import json
import utils
import copy


class Model(object):
    def __init__(self, obj):
        self.model = obj

    @staticmethod
    def from_file(filename):
        return Model(utils.asciify(json.loads(open(filename).read())))

    def get_entity_urls(self):
        """
        >>> m = Model({'hey':{'you':{}},'hi':{} })
        >>> urls = m.get_entity_urls()
        >>> [str(x) for x in urls]
        ['hi', 'hey', 'hey/you']
        """
        return [EntityUrl(self, x) for x in get_dict_names(self.model)]


class EntityUrl(object):
    def __init__(self, model, path):
        self.model = model
        self.path = path

    def name(self):
        return self.path[-1]

    def __str__(self):
        """
        >>> m = Model({})
        >>> e = EntityUrl(m, ['hey', 'you'])
        >>> str(e)
        'hey/you'
        """
        return "/".join(self.path)

    def get_entity_regex(self):
        """

        """
        pass

    def get_entity_properties(self):
        """
        >>> m = Model({'hey':{'you':{'awesome':'yeah'}}})
        >>> e = EntityUrl(m, ['hey', 'you'])
        >>> e.get_entity_properties()
        {'awesome': 'yeah'}
        """
        target = self.model.model
        for path_item in self.path:
            target = target[path_item]
        return target

    def get_entity(self):
        """
        >>> m = Model({'hey':{'you':{'awesome':'string default|chunky'}}})
        >>> e = EntityUrl(m, ['hey', 'you'])
        >>> e = e.get_entity()
        >>> print e.__name__
        you
        """
        return generate_entity(self.name(), self.get_entity_properties())

def get_dict_names(dictionary, list_=None, parents=None):
    """
    Walk through the dict and produce a list of lists,
    where each list is a path to an object.

    >>> get_dict_names({'hey':{'you':{}},'hi':{} })
    [['hi'], ['hey'], ['hey', 'you']]
    >>> get_dict_names({'hey':{'you':{}},'hi':{} })
    [['hi'], ['hey'], ['hey', 'you']]
    """
    if not list_:
        list_ = []
    if not parents:
        parents = []

    for name, property_ in dictionary.iteritems():
        if isinstance(property_, dict):
            temp_parents = copy.deepcopy(parents)
            temp_parents.append(name)
            list_.append(temp_parents)
            list_ = get_dict_names(dictionary[name], list_, temp_parents)
    return list_



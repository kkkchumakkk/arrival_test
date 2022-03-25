import random
import string
import json

from arrival_test.alaska_api.constants import FIELD_BEAR_TYPE, FIELD_BEAR_NAME, FIELD_BEAR_AGE


class Bear:
    """
    Class that represents record in DB
    """
    DEFAULT_BEAR_NAME_LENGTH = 10
    ALLOWED_BEAR_AGE_INTERVAL = (0, 100)
    DEFAULT_AGE_PRECISION = 2

    BEAR_TYPE_POLAR = "POLAR"
    BEAR_TYPE_BROWN = "BROWN"
    BEAR_TYPE_BLACK = "BLACK"
    BEAR_TYPE_GUMMY = "GUMMY"

    AVAILABLE_BEAR_TYPES = (BEAR_TYPE_POLAR, BEAR_TYPE_BROWN, BEAR_TYPE_BLACK, BEAR_TYPE_GUMMY)

    def __init__(self, bear_type=None, bear_name=None, bear_age=None, bear_id=None):
        self.type = bear_type if bear_type != None else random.choice(self.AVAILABLE_BEAR_TYPES)
        self.name = bear_name if bear_name != None else ''.join(random.choices(string.ascii_letters,
                                                                       k=self.DEFAULT_BEAR_NAME_LENGTH))
        self.age = bear_age if bear_age != None else round(random.uniform(*self.ALLOWED_BEAR_AGE_INTERVAL),
                                                   self.DEFAULT_AGE_PRECISION)
        self.id = bear_id

    def __eq__(self, obj):
        return not self.get_diff(obj)

    def __str__(self):
        return f'Bear type: {self.type}. Bear age: {self.age}. Bear name: {self.name}.'

    __repr__ = __str__

    def json_repr(self):
        """
        Method that converts instance of Bear class into json string

        @return: json string
        """
        return json.dumps(dict(zip((FIELD_BEAR_TYPE, FIELD_BEAR_NAME, FIELD_BEAR_AGE), (self.type, self.name, self.age))))

    def get_diff(self, obj):
        """
        Method that compares two instances of Bear class

        @return: string that contains differences between instances

        @param obj: instance of Bear class
        """
        diff_msg = ''
        if self.type != obj.type:
            diff_msg += f'Bear types does not match. {self.type} != {obj.type}'
        if self.age != obj.age:
            diff_msg += f'Bear names not match. {self.age} != {obj.age}'
        if self.name != obj.name:
            diff_msg += f'Bear ages does not match. {self.name} != {obj.name}'
        if self.id and obj.id and self.id != obj.id:
            diff_msg += f'Bear ids does not match. {self.id} != {obj.id}'
        return diff_msg


class BearsGroup:
    """
    Class that represents collection of Bear instances
    """
    def __init__(self, bears_data):
        self.bears = [Bear(**bear_data) for bear_data in bears_data]

    def __add__(self, new_bear):
        self.bears.append(new_bear)

    def __contains__(self, other):
        for bear in self.bears:
            if bear == other:
                return True
        return False

    def __eq__(self, obj):
        for bear in self.bears:
            if bear not in obj.bears:
                return False
        return True

    def __repr__(self):
        str_repr = ''
        for bear in self.bears:
            str_repr += str(bear) + ';'
        return f'[{str_repr}]\n'

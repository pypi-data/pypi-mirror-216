from enum import Enum


class Option:
    class Separators(Enum):
        SPACE = 'S'
        EQUAL = '='

    def __init__(
            self,
            name: str,
            description: str,
            short: str = ''
    ):
        self.name = name
        self.description = description
        self.short = short
        self.var_name = ''
        self._var_type = bool
        self.value = None

    def __str__(self):
        return f'[{self.__class__.__name__}]{self.name}: {self.value}'

    def __repr__(self):
        return f'[{self.__class__.__name__}]{self.name}: {self.value}'

    @property
    def var_type(self):
        return self._var_type

    @var_type.setter
    def var_type(self, name):
        ret = None
        match name:
            case 'str': ret = str
            case 'int': ret = int
            case 'float': ret = float
            case _: ret = bool
        self._var_type = ret

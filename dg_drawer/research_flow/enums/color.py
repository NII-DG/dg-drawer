from enum import Enum
from dg_drawer.error.error import EnumValueError

class ColorType(Enum):
    """Colour type (enumerated type)
    """
    GREY = (0, '#616161', '#BDBDBD')
    TEAL = (1, '#00796B', '#B2DFDB')
    RED = (2, '#D32F2F', '#FFCDD2')
    INDIGO = (3, '#303F9F', '#C5CAE9')
    DEEP_ORANGE = (4, '#E64A19', '#FFCCBC')
    GREEN = (5, '#388E3C', '#C8E6C9')
    CYAN = (6, '#0097A7', '#B2EBF2')
    AMBER = (7, '#FFA000', '#FFECB3')
    DEEP_PURPLE = (8, '#512DA8', '#D1C4E9')

    @classmethod
    def get_phase_color_by_index(cls, index:int)->str:
        """Obtain colour code for phase

        Args:
            index (int): [colour index]

        Raises:
            EnumValueError: [Error if Index not defined]

        Returns:
            str: [colour code]
        """
        for e in ColorType:
            if e.value[0] == index:
                return e.value[1]
        raise EnumValueError('{} is not defined in Color Class.'.format(index))

    @classmethod
    def get_phase_node_by_index(cls, index:int):
        """Obtain colour code for node

        Args:
            index (int): [colour index]

        Raises:
            EnumValueError: [Error if Index not defined]

        Returns:
            [type]: [colour code]
        """
        for e in ColorType:
            if e.value[0] == index:
                return e.value[2]
        raise EnumValueError('{} is not defined in Color Class.'.format(index))

from PyExpansion.common import utils
from PyExpansion.application.PyCarPlate import status_code_list


class PyCarPlateBase(utils.BaseClass):
    symbol_represent = {}  # symbol that use in car plate
    length_car_plates = []  # list of the length of the car plates
    patterns = []  # list of pattern of the car plates

    def __init__(self, car_plate: str):
        self.car_plate = car_plate

    def _valid_same_length(self):
        from PyExpansion.common.data_type.lists import main as lists_main
        response = lists_main.ListExpansion.compare_two_list_length(self.length_car_plates, self.patterns)
        self.error_code = response["code"]
        return False if not response["info"] else True

    def _check_pattern_is_valid(self):
        for count, pattern in enumerate(self.patterns):
            if len(pattern) != self.length_car_plates[count]:
                return False

        return True

    def _check_pattern_in_symbol(self):
        for pattern in self.patterns:
            for pattern_word in pattern:
                if pattern_word not in self.symbol_represent.keys():
                    return False
        return True

    def _verify(self):
        pass

from PyExpansion.application.PyCarPlate.country import base


class PyMalaysiaCarPlate(base.PyCarPlateBase):
    symbol_represent = {
        "C": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "N": "0123456789",
        "S": ["1M4U", "PATRIOT"],
    } # symbol that use in car plate
    length_plate = [7, 7]
    pattern = ["CCCNNNN", "CCNNNNC"]

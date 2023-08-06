from PyExpansion.application.PyCarPlate import main

test_case_material = [
    {
       "country": "M",
       "ic_word": "123456478",
       "test_condition": "Invalid Country",
       "special": "",
    },
]

for count, x in enumerate(test_case_material, start=1):
    try:
        del test_case
    except NameError:
        pass
    test_case = main.PyCarPlate(x["country"], x["ic_word"])
    print("Case %s: " % str(count), test_case.get_detail())
    print("Error Check Case %s: " % str(count), test_case.check_error())
    if x["special"]:
        print("This function ", x["special"])


def parse_check_value(input):

    if type(input) is bool:
        if input:
            return 2
        return 0
    elif type(input) is int:
        if input == 2:
            return True
        return False
    else:
        return bool(input)

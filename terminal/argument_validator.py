def is_valid_int(input: str) -> bool:
    if not is_valid_str(input):
        return False
    
    try:
        _ = int(input)
        return True
    except:
        return False
    
def is_valid_dimension(input: str) -> bool:
    if not is_valid_str(input):
        return False
    
    try:
        input = input.lower()

        if 'x' not in input:
            return False
        
        i_x = input.find('x')
        width = input[:i_x]
        length = input[i_x + 1:]
        print(f' {width} - {length}')
        if not is_valid_float(width) or not is_valid_float(length):
            return False
        
        return True
    except:
        print('error')
        return False

def is_valid_float(input: str) -> bool:
    if not is_valid_str(input):
        return False
    
    try:
        _ = float(input)
        return True
    except:
        return False

def is_valid_str(input: str):
    if isinstance(input, str) and len(input) > 0:
        return True
    return False
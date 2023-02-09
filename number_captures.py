from talon import Module

module = Module()
@module.capture(rule = '<number> (point|dot) <number>')
def diagram_drawing_decimal_number(m) -> str:
    ''''''
    number: str = str(m[0]) + '.' + str(m[2])
    return number

@module.capture(rule = '<number>|<user.diagram_drawing_decimal_number>')
def diagram_drawing_positive_number(m) -> str:
    ''''''
    try:
        return m.diagram_drawing_decimal_number
    except:
        pass
    return str(m.number)

@module.capture(rule = '[dash|minus|negative] <user.diagram_drawing_positive_number>')
def diagram_drawing_number(m) -> str:
    ''''''
    return compute_signed_number_string_for_capture(m)
    
@module.capture(rule = '<user.diagram_drawing_number>')
def diagram_drawing_number_float(m) -> float:
    ''''''
    result: float = float(m.diagram_drawing_number)
    return result

@module.capture(rule = '<number_small> (point|dot) <number_small>')
def diagram_drawing_small_decimal_number(m) -> str:
    number: str = str(m[0]) + '.' + str(m[2])
    return number

@module.capture(rule = '<number_small>|<user.diagram_drawing_small_decimal_number>')
def diagram_drawing_small_positive_number(m)-> str:
    ''''''
    try:
        return m.diagram_drawing_small_decimal_number
    except:
        pass
    return str(m.number_small)

@module.capture(rule = '[dash|minus|negative] <user.diagram_drawing_small_positive_number>')
def diagram_drawing_small_number(m) -> str:
    ''''''
    return compute_signed_number_string_for_capture(m)

@module.capture(rule = '<user.diagram_drawing_small_number>')
def diagram_drawing_small_float(m) -> float:
    ''''''
    result: float = float(m.diagram_drawing_small_number)
    return result

def compute_signed_number_string_for_capture(m):
    result: str = m[0]
    if len(m) == 2:
        result = '-' + m[1]
    return result

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
    result: str = m[0]
    if len(m) == 2:
        result = '-' + m[1]
    return result

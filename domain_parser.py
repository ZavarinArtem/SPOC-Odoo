
def parse_domain(domain):
    data = {
        'domain': domain,
        'index': 0,
    }
    return parse_recursively(data)


def parse_recursively(data):

    element = data['domain'][data['index']]
    res = ''
    if type(element) == tuple:
        res = str(element[0]) + ' ' + str(element[1]) + ' \'' + str(element[2]) + '\''
    elif element == '&':
        data['index'] += 1
        res += parse_recursively(data)
        res += '\n AND '
        data['index'] += 1
        res += parse_recursively(data)
    elif element == '|':
        res += '('
        data['index'] += 1
        res += parse_recursively(data)
        res += '\n  OR '
        data['index'] += 1
        res += parse_recursively(data)
        res += ')'
    return res

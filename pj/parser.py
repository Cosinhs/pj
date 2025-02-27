from .constants import *

def parse_array(tokens):
    json_array = []

    if tokens:
        t = tokens[0]
        if t == JSON_RIGHTBRACKET:
            return json_array, tokens[1:]
    else:
        raise Exception('Expected end-of-array bracket')

    while True:
        json, tokens = parse(tokens)
        if type(json) is tuple:
            raise Exception('Invalid element in array')
        json_array.append(json)

        if tokens:
            t = tokens[0]
            if t == JSON_RIGHTBRACKET:
                return json_array, tokens[1:]
            elif t != JSON_COMMA:
                raise Exception('Expected comma after object in array')
            else:
                tokens = tokens[1:]
        else:
            raise Exception('Expected end-of-array bracket')


def parse_object(tokens):
    json_object = {}

    if tokens:
        t = tokens[0]
        if t == JSON_RIGHTBRACE:
            return json_object, tokens[1:]
    else:
        raise Exception('Expected end-of-object bracket')

    while True:
        if tokens:
            json_key = tokens[0]
            if type(json_key) is str:
                tokens = tokens[1:]
            else:
                raise Exception('Expected string key, got: {}'.format(json_key))
        else:
            raise Exception('Expected string key')

        if tokens:
            t = tokens[0]
            if t != JSON_COLON:
                raise Exception('Expected colon after key in object, got: {}'.format(t))

            json_value, tokens = parse(tokens[1:])

            json_object[json_key] = json_value

            if tokens:
                t = tokens[0]
                if t == JSON_RIGHTBRACE:
                    return json_object, tokens[1:]
                elif t != JSON_COMMA:
                    raise Exception('Expected comma after pair in object, got: {}'.format(t))
                else:
                    tokens = tokens[1:]
            else:
                raise Exception('Expected comma or end-of-object bracket')
        else:
            raise Exception('Expected colon after key in object')

def parse(tokens, is_root=False):
    if tokens:
        t = tokens[0]

        if is_root and t != JSON_LEFTBRACE:
            raise Exception('Root must be an object')

        if t == JSON_LEFTBRACKET:
            return parse_array(tokens[1:])
        elif t == JSON_LEFTBRACE:
            return parse_object(tokens[1:])
        else:
            return t, tokens[1:]
    else:
        raise Exception('Expected json element')

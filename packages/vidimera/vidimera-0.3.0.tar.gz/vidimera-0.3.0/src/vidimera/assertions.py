from .behaviour import Behaviour


def assert_implements(obj, expected, scope=Behaviour.PUBLIC_AND_SPECIAL):
    if delta := Behaviour(obj).implements(expected, scope=scope):
        return delta
    else:
        raise AssertionError(str(delta))

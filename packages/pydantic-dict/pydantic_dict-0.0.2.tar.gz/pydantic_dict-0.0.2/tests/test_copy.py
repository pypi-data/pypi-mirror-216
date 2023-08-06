import copy


class Sent:
    def __copy__(self):
        return self

    def __deepcopy__(self, *args, **kwargs):
        return self


s = Sent()


def test_copy():
    j = copy.deepcopy(s)
    assert s == j

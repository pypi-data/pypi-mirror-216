"""
This file is for storing string objects as USD and then be able to do various things with them.
class Foo(object):
    def __init__(self):
        self._bar = 0

    bar = property(lambda self: self._bar + 5)
"""


class USDString(str):
    """Class for strings in united-states dollars."""
    def __new__(cls, *args, **kwargs):
        setattr(cls, 'text', None)
        cls.text = None
        if isinstance(cls, str):
            return
        if isinstance(cls, float):
            return
        if isinstance(cls, int):
            return
        cls.__init__(*args, **kwargs)

    def __repr__(self):
        return self.billions().millions().thousands().decimals().text

    def __str__(self):
        return self.text

    def __add__(self, other):
        return str(self.text + other)

    def thousands(self):
        return self.replace(',', 'K')

    def millions(self):
        return self.replace(',', 'M')

    def billions(self):
        return self.replace(',', 'B')

    def decimals(self):
        return '${:,.2f}'.format(self)

a = USDString('ysdf')
b = USDString('002')
c = USDString(3333)
print(repr(a))
print(str(b))
print(a + b)
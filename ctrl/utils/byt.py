#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  
#  CTRL - Ground-Segment software for Cube-Sats
#  Copyright (C) 2016-2017  Guillaume Schworer
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
#  For any information, bug report, idea, donation, hug, beer, please contact
#    guillaume.schworer@gmail.com
#
###############################################################################


from sys import version_info
PYTHON3 = version_info > (3,)


__all__ = ['Byt']


if PYTHON3:

    class Byt(bytes):
        def __new__(cls, value=''):
            if isinstance(value, str):
                # It's a unicode string:
                value = value.encode('ISO-8859-1')
            elif isinstance(value, int):
                value = chr(value).encode('ISO-8859-1')
            return super().__new__(cls, value)

        def __getitem__(self, pos):
            if isinstance(pos, int):
                return Byt(super().__getitem__(pos))
            else:
                return Byt(super().__getitem__(pos))

        def __eq__(self, other):
            if not isinstance(other, Byt):
                if isinstance(other, (str, bytes)):
                    raise TypeError("can't compare Byt and " +
                                        type(other).__name__)
                else:
                    return False
            else:
                return super().__eq__(other)

        def __ne__(self, other):
            if not isinstance(other, Byt):
                if isinstance(other, (str, bytes)):
                    raise TypeError("can't compare Byt and " +
                                        type(other).__name__)
                else:
                    return True
            else:
                return super().__ne__(other)

        def __str__(self):
            return self.decode('ISO-8859-1')

        def __hash__(self):
            return super().__hash__()

        def __repr__(self):
            return "{}('{}')".format(self.__class__.__name__, self.__str__())

        def __iter__(self):
            for ch in super().__iter__():
                yield Byt(ch)

        def __add__(self, txt):
            if not isinstance(txt, Byt):
                raise TypeError("can't concat Byt to " + type(txt).__name__)
            return Byt(super().__add__(txt))

        def __radd__(self, txt):
            if not isinstance(txt, Byt):
                raise TypeError("can't concat Byt to " + type(txt).__name__)
            return Byt(txt.__add__(self))

        def __mul__(self, other):
            return Byt(super().__mul__(other))

        def __rmul__(self, other):
            return Byt(super().__rmul__(other))

        def __contains__(self, other):
            if not isinstance(other, Byt):
                if isinstance(other, (str, bytes)):
                    raise TypeError("can't compare Byt to " +
                                        type(other).__name__)
                else:
                    return False
            else:
                return super().__contains__(other)

        def iterInts(self):
            """
            Returns the iterator of ints
            """
            for ch in super().__iter__():
                yield ch

        def ints(self):
            """
            Returns the list of ints
            """
            return list(self.iterInts())

        def hex(self):
            return ' '.join(super(Byt, ch).hex() for ch in self)

        def split(self, sep=None, maxsplit=-1):
            if not isinstance(sep, Byt) and sep is not None:
                raise TypeError("can't split Byt and " + type(sep).__name__)
            return list(map(Byt, super().split(sep, maxsplit)))

        def rsplit(self, sep=None, maxsplit=-1):
            if not isinstance(sep, Byt) and sep is not None:
                raise TypeError("can't rsplit Byt and " + type(sep).__name__)
            return list(map(Byt, super().rsplit(sep, maxsplit)))

        def replace(self, old, new, count=-1):
            if not isinstance(old, Byt) or not isinstance(new, Byt):
                raise TypeError("can't replace with non-Byt characters")
            return Byt(super().replace(old, new, count))

        def zfill(self, width):
            return Byt(super().zfill(width))

        def strip(self, bytes=None):
            if not isinstance(bytes, Byt) and bytes is not None:
                raise TypeError("can't strip Byt and " + type(bytes).__name__)
            return Byt(super().strip(bytes))

        def lstrip(self, bytes=None):
            if not isinstance(bytes, Byt) and bytes is not None:
                raise TypeError("can't lstrip Byt and " + type(bytes).__name__)
            return Byt(super().lstrip(bytes))

        def rstrip(self, bytes=None):
            if not isinstance(bytes, Byt) and bytes is not None:
                raise TypeError("can't rstrip Byt and " + type(bytes).__name__)
            return Byt(super().rstrip(bytes))

        def join(self, iterable_of_bytes):
            if len(iterable_of_bytes) == 0:
                return Byt()
            for item in iterable_of_bytes:
                if not isinstance(item, Byt):
                    raise TypeError("can't join non-Byt characters")
            else:
                return Byt(super().join(iterable_of_bytes))

else:

    from binascii import hexlify
    from types import GeneratorType

    class Byt(str):
        def __new__(cls, value=''):
            if isinstance(value, int):
                value = chr(value)
            elif isinstance(value, GeneratorType):
                value = list(value)
            if len(value) > 0:
                if isinstance(value[0], int):
                    # It's a list of integers
                    value = ''.join(chr(item) for item in value)
            return super(Byt, cls).__new__(cls, value)

        def __getitem__(self, pos):
            return Byt(super(Byt, self).__getitem__(pos))

        def __getslice__(self, deb, fin):
            return Byt(super(Byt, self).__getslice__(deb, fin))

        def __eq__(self, other):
            if not isinstance(other, Byt):
                if isinstance(other, (str, unicode)):
                    raise TypeError("can't compare Byt and " +
                                        type(other).__name__)
                else:
                    return False
            else:
                return super(Byt, self).__eq__(other)

        def __ne__(self, other):
            if not isinstance(other, Byt):
                if isinstance(other, (str, unicode)):
                    raise TypeError("can't compare Byt and " +
                                        type(other).__name__)
            else:
                return super(Byt, self).__ne__(other)

        def __str__(self):
            return super(Byt, self).__str__()

        def __hash__(self):
            return super(Byt, self).__hash__()

        def __repr__(self):
            return "{}('{}')".format(self.__class__.__name__, self.__str__())

        def __iter__(self):
            for ch in self.__str__():
                yield Byt(ch)

        def __add__(self, txt):
            if not isinstance(txt, Byt):
                raise TypeError("can't concat Byt to " + type(txt).__name__)
            return Byt(super(Byt, self).__add__(txt))

        def __radd__(self, txt):
            if not isinstance(txt, Byt):
                raise TypeError("can't concat Byt to " + type(txt).__name__)
            return txt.__add__(self)

        def __mul__(self, other):
            return Byt(super(Byt, self).__mul__(other))

        def __rmul__(self, other):
            return Byt(super(Byt, self).__rmul__(other))

        def __contains__(self, other):
            if not isinstance(other, Byt):
                if isinstance(other, (str, unicode)):
                    raise TypeError("can't compare Byt to " +
                                        type(other).__name__)
                else:
                    return False
            else:
                return super(Byt, self).__contains__(other)

        def iterInts(self):
            """
            Returns the iterator of ints
            """
            for ch in self.__str__():
                yield ord(ch)

        def ints(self):
            """
            Returns the list of ints
            """
            return list(self.iterInts())

        def hex(self):
            return ' '.join(hexlify(ch) for ch in self)

        def split(self, sep=None, maxsplit=-1):
            if not isinstance(sep, Byt) and sep is not None:
                raise TypeError("can't split Byt and " + type(sep).__name__)
            return list(map(Byt, super(Byt, self).split(sep, maxsplit)))

        def rsplit(self, sep=None, maxsplit=-1):
            if not isinstance(sep, Byt) and sep is not None:
                raise TypeError("can't rsplit Byt and " + type(sep).__name__)
            return list(map(Byt, super(Byt, self).rsplit(sep, maxsplit)))

        def replace(self, old, new, count=-1):
            if not isinstance(old, Byt) or not isinstance(new, Byt):
                raise TypeError("can't replace with non-Byt characters")
            return Byt(super(Byt, self).replace(old, new, count))

        def zfill(self, width):
            return Byt(super(Byt, self).zfill(width))

        def strip(self, bytes=None):
            if not isinstance(bytes, Byt) and bytes is not None:
                raise TypeError("can't strip Byt and " + type(bytes).__name__)
            return Byt(super(Byt, self).strip(bytes))

        def lstrip(self, bytes=None):
            if not isinstance(bytes, Byt) and bytes is not None:
                raise TypeError("can't strip Byt and " + type(bytes).__name__)
            return Byt(super(Byt, self).lstrip(bytes))

        def rstrip(self, bytes=None):
            if not isinstance(bytes, Byt) and bytes is not None:
                raise TypeError("can't strip Byt and " + type(bytes).__name__)
            return Byt(super(Byt, self).rstrip(bytes))

        def join(self, iterable_of_bytes):
            if len(iterable_of_bytes) == 0:
                return Byt()
            for item in iterable_of_bytes:
                if not isinstance(item, Byt):
                    raise TypeError("can't join non-Byt characters")
            else:
                return Byt(super(Byt, self).join(iterable_of_bytes))

# test.py

import time
import warnings

from pystatic.overload import overload
from pystatic.types import statictypes
from pystatic.private import private
from pystatic.casting import cast

class Demo1:

    def __init__(self, a, b, c, x=None):

        self.a = a
        self.b = b
        self.c = c
        self.x = x

class Demo2(Demo1):

    def __init__(self, a, b, c, x=None, y=None, z=None):

        super().__init__(a, b, c, x)

        self.y = y
        self.z = z

demo2 = Demo2(0, 1, 2, 3, 4, 5)
demo1 = cast(Demo1, demo2)

print(demo2, type(demo2), demo2.__dict__)
print(demo1, type(demo1), demo1.__dict__)

# noinspection PyNestedDecorators
class Foo:

    c = private()

    def __init__(self):

        print("\nclass Foo:\n\n\tdef __init__(self):\n")

        self.c = 1
        print("\t\t>>> self.c = 1")
        print("\t\t>>> print(self.c)")
        print(f"\t\t{self.c}\n")

        self.c = 0
        print("\t\t>>> self.c = 0")
        print("\t\t>>> print(self.c)")
        print(f"\t\t{self.c}\n")

        self.__d = 0
        print("\t\t>>> self.__d = 0")
        print("\t\t>>> print(self.__d)")
        print(f"\t\t{self.__d}\n")

    @overload
    def a(self):
        pass

    @a.overload
    def a(self, x: int):
        print("\n\tdef a(self, x: int):")
        print(f"\n\t\t>>> print(type(x))")
        print(f"\t\t{type(x)}\n")

    @a.overload
    def a(self, x: str):
        print("\n\tdef a(self, x: str):")
        print(f"\n\t\t>>> print(type(x))")
        print(f"\t\t{type(x)}\n")

    @a.overload
    @staticmethod
    def a(x: float):
        print("\n\t@staticmethod\n\tdef a(x: float):")
        print(f"\n\t\t>>> print(type(x))")
        print(f"\t\t{type(x)}\n")

    @a.overload
    @classmethod
    def a(cls, x: float):
        print("\n\t@classmethod\n\tdef a(cls, x: float):")
        print(f"\n\t\t>>> print(type(x))")
        print(f"\t\t{type(x)}\n")

    @statictypes(crush=False)
    def b(self, x: int):
        print("\n\t@statictypes(crush=False)\n\tdef b(self, x: int):")
        print(f"\n\t\t>>> print(type(x))")
        print(f"\t\t{type(x)}\n")

foo = Foo()

print(">>> foo.a('')")
foo.a('')
print(">>> foo.a(0.0)")
foo.a(0.0)
print(">>> Foo.a(0)")
Foo.a(0)
print(">>> Foo.a(0.0)")
Foo.a(0.0)

print(">>> foo.b(0)")
foo.b(0)
print(">>> foo.b(0.0)")
# noinspection PyTypeChecker
foo.b(0.0)

time.sleep(0.2)

try:
    print("\n>>> print(Foo.c)")
    print(Foo.c)

except AttributeError as e:
    warnings.warn(str(e))
# end try

time.sleep(0.2)

try:
    print("\n>>> print(foo.c)")
    print(foo.c)

except AttributeError as e:
    warnings.warn(str(e))
# end try

time.sleep(0.2)
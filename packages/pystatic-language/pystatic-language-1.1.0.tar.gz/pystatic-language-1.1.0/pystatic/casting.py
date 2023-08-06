# casting.py

from typing import (
    Type, Any, TypeVar, Optional, Iterable
)

import dill

__all__ = [
    "cast",
    "copy",
    "deepcopy",
    "CastType",
    "castable"
]

_T = TypeVar("_T")
_O = TypeVar("_O")

class CastType:
    """A class to represent a casting type mechanism."""

    def __init__(self, base: Type[_T]) -> None:
        """
        Defines the class attributes.

        :param base: The type to cast the object into.
        """

        self.base = base
    # end __init__

    def __call__(self, instance: _O, attributes: Optional[Iterable[str]] = None) -> _T:
        """
        Creates a casting mechanism for casting objects into different types.

        :param instance: The object instance to cast into the new type.
        :param attributes: The attributes to include.

        :return: The new object of the new type.
        """

        if attributes is None:
            attributes = list(instance.__dict__)
        # end if

        try:
            new_instance = self.base.__new__(self.base)

            new_instance.__dict__.update(
                {
                    key: value for key, value in instance.__dict__.items()
                    if key in attributes
                }
            )

            return new_instance

        except (ValueError, TypeError) as e:
            raise TypeError(
                f"Cannot cast {repr(instance)} into "
                f"{repr(self.base)}. {str(e)}"
            )
        # end try
    # end __call__
# end CastType

def castable(base: Type[_T]) -> CastType:
    """
    Creates a casting mechanism for casting objects into different types.

    :param base: The type to cast the object into.

    :return: The new object of the new type.
    """

    return CastType(base=base)
# end castable

def cast(base: Type[_T], instance: _O, attributes: Optional[Iterable[str]] = None) -> _T:
    """
    Creates a casting mechanism for casting objects into different types.

    :param base: The type to cast the object into.
    :param instance: The object instance to cast into the new type.
    :param attributes: The attributes to include.

    :return: The new object of the new type.
    """

    return castable(base=base)(instance=instance, attributes=attributes)
# end cast

def copy(instance: Any) -> Any:
    """
    Creates a copy mechanism for copying objects.

    :param instance: The object instance to copy.

    :return: The new object copy.
    """

    return cast(type(instance), instance=instance)
# end copy

def deepcopy(instance: Any) -> Any:
    """
    Creates a deep copy mechanism for copying objects.

    :param instance: The object instance to copy.

    :return: The new object copy.
    """

    return dill.loads(dill.dumps(instance))
# end deepcopy
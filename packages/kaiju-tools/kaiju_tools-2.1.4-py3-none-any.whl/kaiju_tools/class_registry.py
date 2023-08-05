"""Class registries for dynamic object creation."""

import abc
import inspect
from collections.abc import Mapping
from typing import Union, Type, Collection

__all__ = ('AbstractClassRegistry', 'ClassRegistrationError')


class _AbstractClassRegistryMeta(abc.ABCMeta):
    def __init__(cls, *args, **kws):
        super().__init__(*args, **kws)
        if abc.ABC not in cls.__bases__:
            cls._validate_class_manager(cls)

    @staticmethod
    def _validate_class_manager(cls):
        if not cls.base_classes:
            raise ValueError('%s.base_classes attribute must be provided.' % cls.__qualname__)
        elif not isinstance(cls.base_classes, Collection):
            raise ValueError('%s.base_classes must be a collection.' % cls.__qualname__)
        else:
            cls.base_classes = tuple(cls.base_classes)


class ClassRegistrationError(TypeError):
    """Error during registration of a class in a registry."""


class AbstractClassRegistry(Mapping, abc.ABC, metaclass=_AbstractClassRegistryMeta):
    """Class manager with the ability to register and store other classes in its own class mapping.

    Because it's a subclass of `Mapping`, it can be serialized into a dictionary
    and implements most of `dict` methods except `__setitem__`.

    :param classes: optional initial list of classes (they will be registered automatically)
    :param raise_if_exists: raise a `ClassRegistrationError` error if class is being registered twice
    """

    base_classes = None  #: a tuple of base classes
    RAISE_IF_EXISTS = False  #: defaults

    def __init__(self, *classes, raise_if_exists: bool = RAISE_IF_EXISTS):
        if classes:
            for cls in classes:
                self.register_class(cls)
        self._classes = classes if classes else {}
        self._raise_if_exists = raise_if_exists

    def __contains__(self, item: Union[str, Type]):
        if inspect.isclass(item) and issubclass(item, self.base_classes):
            return self.class_key(item) in self._classes
        else:
            return item in self._classes

    def __getitem__(self, item: str) -> Type:
        return self._classes[item]

    def __getattr__(self, item: str) -> Type:
        if item in self:
            return self[item]
        else:
            return getattr(super(), item)

    def get(self, key: str, default=None):
        """Call `dict().get` method."""
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(self):
        return iter(self._classes.keys())

    def __len__(self):
        return len(self._classes)

    def can_register(self, obj: Type) -> bool:
        """Check if an object can be registered."""
        try:
            self._validate_class(obj)
        except ClassRegistrationError:
            return False
        else:
            return True

    @staticmethod
    def class_key(obj) -> str:
        """Get a name by which a class will be referenced in the registry."""
        if inspect.isclass(obj):
            return obj.__name__
        else:
            return obj.__class__.__name__

    def register_class(self, obj: Type):
        """Register a new service class in the service context manager.

        :raises ClassRegistrationError: if the class can't be registered
        """
        self._validate_class(obj)
        self._register_class(obj)

    def register_classes_from_globals(self):
        """Call `register_classes_from_namespace(globals())`."""
        return self.register_classes_from_namespace(globals())

    def register_classes_from_module(self, module):
        """Call `register_classes_from_namespace(module.__dict__)`."""
        return self.register_classes_from_namespace(module.__dict__)

    def register_classes_from_namespace(self, namespace: dict):
        """Register all supported classes from a mapping.

        Incompatible data will be ignored.
        """
        for obj in namespace.values():
            if self.can_register(obj):
                self._register_class(obj)

    def _validate_class(self, obj):
        if not inspect.isclass(obj):
            raise ClassRegistrationError(f'Can\'t register object {obj} because it\'s not a class.')
        elif inspect.isabstract(obj) or abc.ABC in obj.__bases__:
            raise ClassRegistrationError(f'Can\'t register object {obj} because it\'s an abstract class.')
        elif not issubclass(obj, self.base_classes):
            raise ClassRegistrationError(
                f'Can\'t register object {obj} because it\'s not a subclass'
                f' of any of the base classes {self.base_classes}'
            )
        elif self.class_key(obj) in self:
            if self._raise_if_exists:
                raise ClassRegistrationError(
                    f'Can\'t register class {obj} because a class with the same' f' name was already registered.'
                )
            # else:
            #     warnings.warn(
            #         f'Class with a name {obj.__name__} was registered twice. This may cause'
            #         f' errors. Conflicting classes: {obj} and {self[self.class_key(obj)]}.'
            #         f' You may change this behavior by setting "raise_if_exists" parameter'
            #         f' to False in the class registry settings.'
            #     )

    def _register_class(self, obj: Type):
        self._classes[self.class_key(obj)] = obj

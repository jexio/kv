import sys
from collections import defaultdict
from typing import Callable, Dict, Iterable, ParamSpec, Tuple


P = ParamSpec("P")


class Registry:
    """Registry of pipeline's components: models, datasets, metrics, etc.
    The registry is meant to be used as a decorator for any classes or function,
    so that they can be accessed by class name for instantiating.

    Examples:
        COMPONENTS = Registry('components')
        @COMPONENTS.register_class
        class SomeComponent:
            ...
    """

    def __init__(self, name: str) -> None:
        """Create a new instance of Registry.

        Args:
            name: Component name.
        """
        self._name = name
        self._entrypoints: Dict[str, Callable] = {}  # mapping of class/function names to entrypoint fns
        self._object_to_module: Dict[str, str] = {}  # mapping of class/function names to its module name
        self._module_to_objects = defaultdict(set)  # dict of sets to check membership of class/function in module

    def __repr__(self) -> str:
        format_str = self.__class__.__name__
        format_str += f"(name={self._name}, items={list(self._entrypoints)})"
        return format_str

    def __contains__(self, item: str) -> bool:
        return item in self._entrypoints

    def __getitem__(self, key: str) -> Callable:
        return self.get(key)

    def __iter__(self) -> Iterable[Tuple[str, Callable]]:
        for key, value in self._entrypoints.items():
            yield key, value

    def get(self, key: str) -> Callable:
        """Search class type by class name.

        Args:
            key: Component class name.

        Returns:
            Found class type.

        Raises:
            KeyError: If key not in dictionary.
        """
        if key not in self._entrypoints:
            raise KeyError(f"{key} is not in the {self._name} registry")

        result = self._entrypoints[key]

        return result

    def register_class(self, fn: Callable) -> Callable:
        """Register a new entrypoint.

        Args:
            fn: function to be registered.

        Raises:
            TypeError: If fn is not callable.
            KeyError: If class_type is already registered.

        Returns:
            Input callable object.
        """
        if not callable(fn):
            raise TypeError(f"{fn} must be callable")
        class_name = fn.__name__
        if class_name in self._entrypoints:
            raise KeyError(f"{class_name} is already registered in {self._name}")

        mod = sys.modules[fn.__module__]
        module_name_split = fn.__module__.split(".")
        module_name = module_name_split[-1] if len(module_name_split) else ""

        # add model to __all__ in module
        model_name = fn.__name__
        if hasattr(mod, "__all__"):
            mod.__all__.append(model_name)
        else:
            mod.__all__ = [model_name]

        # add entries to registry dict/sets
        self._entrypoints[model_name] = fn
        self._object_to_module[model_name] = module_name
        self._module_to_objects[module_name].add(model_name)

        return fn


__all__ = ("Registry",)

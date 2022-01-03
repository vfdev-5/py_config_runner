import ast
import sys
from importlib.machinery import SourceFileLoader

from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Iterator, Mapping, Dict, Optional, Union

from py_config_runner.deprecated import (
    LOGGING_FORMATTER,
    setup_logger,
    add_logger_filehandler,
    set_seed,
)


def load_module(filepath: Union[str, Path]) -> Any:
    """Method to load module from file path

    Args:
        filepath: path to module to load

    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise ValueError(f"File '{filepath.as_posix()}' is not found")

    if not filepath.is_file():
        raise ValueError(f"Path '{filepath.as_posix()}' should be a file")

    return SourceFileLoader(filepath.stem, filepath.as_posix()).load_module()  # type: ignore[call-arg]


class ConfigObject(MutableMapping):
    """Lazy config object

    Args:
        config_filepath: path to python configuration file
        mutations: dict of constant mutations (int, float, str, bool) to apply to the configuration
            python file before loading. See example below.
        kwargs: kwargs to pass to the config object. Note that for colliding keys retained value is
            the one from ``config_filepath``.

    Example:

    .. code-block:: python

        config = ConfigObject("/path/to/baseline.py")
        print(config)
        # For example, configuration file contains params: seed, ...

        print(config.seed, config["seed"], config.get("seed"))

    Example with mutations:

    Let's assume that configuration python file has ``learning_rate = 0.01`` which is used to
    configure an optimizer:

    .. code-block:: python

        # baseline.py configuration file

        learning_rate = 0.01

        optimizer = SGD(parameters, lr=learning_rate)

    And we would like to override ``learning_rate`` from the script using above configuration file
    and has also optimizer updated accordingly:

    .. code-block:: python

        # Script file using baseline.py configuration

        config = ConfigObject("/path/to/baseline.py", mutations={"learning_rate": 0.05})
        print(config)
        print(config.optimizer)
        # assert config.optimizer.lr == 0.05

    """

    def __init__(self, config_filepath: Union[str, Path], mutations: Optional[Mapping] = None, **kwargs: Any) -> None:
        if mutations is not None:
            if not (sys.version_info.major >= 3 and sys.version_info.minor >= 7):
                raise RuntimeError("Mutations are not supported on Python versions < 3.7")
            if not isinstance(mutations, Mapping):
                raise TypeError(f"Argument mutations should be a mapping, got {type(mutations)}")

        super().__init__()
        self.__dict__["_is_loaded"] = False
        self.__dict__["_mutations"] = mutations
        self.__dict__["__internal_config_object_data_dict__"] = {"config_filepath": config_filepath}
        self.__dict__["__internal_config_object_data_dict__"].update(kwargs)

    def __getattr__(self, item: Any) -> Any:
        self._load_if_not()
        return self.__internal_config_object_data_dict__[item]

    def __setattr__(self, name: str, value: Any) -> None:
        self._load_if_not()
        self.__internal_config_object_data_dict__[name] = value

    def __len__(self) -> int:
        self._load_if_not()
        return len(self.__internal_config_object_data_dict__)

    def __getitem__(self, item: Any) -> Any:
        self._load_if_not()
        return self.__internal_config_object_data_dict__[item]

    def __setitem__(self, name: Any, value: Any) -> None:
        self._load_if_not()
        self.__internal_config_object_data_dict__[name] = value

    def __delitem__(self, key) -> None:
        self._load_if_not()
        del self.__internal_config_object_data_dict__[key]

    def __iter__(self) -> Iterator:
        self._load_if_not()
        return iter(self.__internal_config_object_data_dict__)

    def get(self, item: Any, default_value: Optional[Any] = None) -> Any:
        self._load_if_not()
        return self.__internal_config_object_data_dict__.get(item, default_value)

    def __contains__(self, item: Any) -> bool:
        self._load_if_not()
        return item in self.__internal_config_object_data_dict__

    def _load_if_not(self) -> None:
        if self.__dict__["_is_loaded"]:
            return
        cfpath = self.__internal_config_object_data_dict__["config_filepath"]
        mutations = self.__dict__["_mutations"]
        if mutations is None or len(mutations) < 1:
            mod_obj = load_module(cfpath)
            _config = mod_obj.__dict__
        else:
            _config = self._apply_mutations_and_load(cfpath, mutations)

        self.__internal_config_object_data_dict__.update({k: v for k, v in _config.items() if not k.startswith("__")})
        self.__dict__["_is_loaded"] = True

    def _apply_mutations_and_load(self, filepath: Union[str, Path], mutations: Mapping) -> Mapping:
        filepath = Path(filepath)
        if not filepath.exists():
            raise ValueError(f"File '{filepath.as_posix()}' is not found")

        if not filepath.is_file():
            raise ValueError(f"Path '{filepath.as_posix()}' should be a file")

        with filepath.open("r") as h:
            config_source = h.read()

        ast_obj = ast.parse(config_source)
        if sys.version_info.major == 3 and sys.version_info.minor < 8:
            mutator: _ConstMutator = _ConstMutatorPy37(mutations)
        else:
            mutator = _ConstMutator(mutations)
        mutator.visit(ast_obj)
        mutator.validate()
        compiled_obj = compile(ast_obj, "<string>", "exec")

        config: Dict[str, Any] = {}
        # Config is passed as globals
        exec(compiled_obj, config)
        return config

    def __repr__(self):
        self._load_if_not()
        output = [
            "Configuration:",
        ]
        for k, v in self.items():
            output.append(f"\t{k}: {v}")
        return "\n".join(output)


class _ConstMutator(ast.NodeTransformer):
    def __init__(self, mutations: Mapping):
        self.mutations = mutations
        self._used_mutations = set(self.mutations)

    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        if len(node.targets) == 1 and isinstance(node.value, ast.Constant):
            target = node.targets[0]
            if isinstance(target, ast.Name):
                key = target.id
                if key in self.mutations:
                    node.value.value = self.mutations[key]
                    self._used_mutations.remove(key)
        return node

    def validate(self):
        if len(self._used_mutations) > 0:
            raise RuntimeError(
                f"Following mutations were not applied: {list(self._used_mutations)}. "
                "Please make sure that mutations argument contains correct values. "
                "Otherwise, please open an issue on https://github.com/vfdev-5/py_config_runner/issues/new ."
                "Thank you!"
            )


class _ConstMutatorPy37(_ConstMutator):
    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        if len(node.targets) == 1 and isinstance(node.value, (ast.Num, ast.Str, ast.NameConstant)):
            target = node.targets[0]
            if isinstance(target, ast.Name):
                key = target.id
                if key in self.mutations:
                    if isinstance(node.value, ast.Num):
                        node.value.n = self.mutations[key]
                        self._used_mutations.remove(key)
                    elif isinstance(node.value, ast.Str):
                        node.value.s = self.mutations[key]
                        self._used_mutations.remove(key)
                    elif isinstance(node.value, ast.NameConstant):
                        node.value.value = self.mutations[key]
                        self._used_mutations.remove(key)
        return node

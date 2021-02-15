from importlib.machinery import SourceFileLoader
import sys

from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Callable, Iterator, Optional, Union

from py_config_runner.deprecated import (
    LOGGING_FORMATTER,
    setup_logger,
    add_logger_filehandler,
    set_seed,
)


def load_module(filepath: Union[str, Path]) -> Any:
    """Method to load module from file path

    Args:
        filepath (str or Path): path to module to load

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
        filepath (str or Path): path to python configuration file

    Returns:
        ConfigObject

    Example:

    .. code-block:: python

        config = ConfigObject("/path/to/baseline.py")
        print(config)
        # For example, configuration file contains params: seed, ...

        print(config.seed, config["seed"], config.get("seed"))

    """

    def __init__(self, config_filepath: Union[str, Path], **kwargs: Any) -> None:
        super().__init__()
        self.__dict__["_is_loaded"] = False
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
        _config = load_module(cfpath)
        self.__internal_config_object_data_dict__.update(
            {k: v for k, v in _config.__dict__.items() if not k.startswith("__")}
        )
        self.__dict__["_is_loaded"] = True

    def __repr__(self):
        self._load_if_not()
        output = [
            "Configuration:",
        ]
        for k, v in self.items():
            output.append(f"\t{k}: {v}")
        return "\n".join(output)

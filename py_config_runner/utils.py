import importlib.util

from collections import OrderedDict
from pathlib import Path
from typing import Any, Callable, Optional, Union

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

    spec = importlib.util.spec_from_file_location(filepath.stem, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConfigObject(OrderedDict):
    """Lazy config object
    """

    def __init__(self, config_filepath: Union[str, Path], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._is_loaded = False
        self["config_filepath"] = config_filepath

    def __getitem__(self, item: Any) -> Any:
        self._load_if_not()
        if item in self.__dict__:
            return self.__dict__[item]
        return super().__getitem__(item)

    def __getattr__(self, item: Any) -> Any:
        self._load_if_not()
        if item in self:
            return self[item]
        return self[item]

    def get(self, item: Any, default_value: Optional[Any] = None) -> Any:
        self._load_if_not()
        if item in self.__dict__:
            return self.__dict__[item]
        return super().get(item, default_value)

    def __contains__(self, item: Any) -> bool:
        self._load_if_not()
        return super().__contains__(item) or item in self.__dict__

    def _load_if_not(self) -> None:
        if self._is_loaded:
            return
        _config = load_module(super().__getitem__("config_filepath"))
        self.update(_config.__dict__)
        self._is_loaded = True

import argparse
import json
from typing import Callable, Any

from argtypes.paths import ExistingFile, StrOrPathT

try:
    import yaml
    from yaml.reader import ReaderError

    def YamlFile(Loader=yaml.SafeLoader, *args, **kwargs) -> Callable[[StrOrPathT], Any]:
        def handler(path: StrOrPathT) -> Any:
            path = ExistingFile()(path)

            with path.open('r') as f:
                try:
                    return yaml.load(f, Loader=Loader, *args, **kwargs)

                except Exception as e:
                    raise argparse.ArgumentTypeError(f'unable to load YAML file "{path}": {e}') from e

        return handler

except ModuleNotFoundError:
    pass


def JsonFile(*args, **kwargs) -> Callable[[StrOrPathT], Any]:
    def handler(path: StrOrPathT) -> Any:
        path = ExistingFile()(path)

        with path.open('r') as f:
            try:
                return json.load(f, *args, **kwargs)

            except ReaderError as e:
                raise argparse.ArgumentTypeError(f'unable to load JSON file') from e

    return handler


def TomlFile() -> Callable[[StrOrPathT], Any]:
    pass


def ConfigFile(*args, **kwargs) -> Callable[[StrOrPathT], Any]:
    pass

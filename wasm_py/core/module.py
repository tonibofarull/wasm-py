import logging

from wasm_py.core.function import FunctionType

logger = logging.getLogger(__name__)


class Module:
    def __init__(self) -> None:
        self._types: None | list[FunctionType] = None
        self._type_indices: None | list[int] = None

    def set_types(self, types: list[FunctionType]):
        logger.debug(types)
        self._types = types

    def set_type_indices(self, type_indices: list[int]):
        logger.debug(type_indices)
        self._type_indices = type_indices

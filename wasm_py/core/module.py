import logging

from wasm_py.core.models.function import FunctionType
from wasm_py.core.models.table import TableType

logger = logging.getLogger(__name__)


class Module:
    def __init__(self) -> None:
        self._types: None | list[FunctionType] = None
        self._type_indices: None | list[int] = None
        self._tables: None | list[TableType] = None

    def set_types(self, types: list[FunctionType]):
        logger.debug(types)
        self._types = types

    def set_type_indices(self, type_indices: list[int]):
        logger.debug(type_indices)
        self._type_indices = type_indices

    def set_tables(self, tables: list[TableType]):
        logger.debug(tables)
        self._tables = tables

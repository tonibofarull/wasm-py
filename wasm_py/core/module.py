from wasm_py.core.function import FunctionType


class Module:
    def __init__(self) -> None:
        self._types: None | list[FunctionType] = None
        self._type_indices: None | list[int] = None

    def set_types(self, types: list[FunctionType]):
        print(types)
        self._types = types

    def set_type_indices(self, type_indices: list[int]):
        print(type_indices)
        self._type_indices = type_indices

from typing import Any

class ApiError(Exception):
    """GeometricalLayoutApi error"""
    def __init__(self, message: str, code: Any = None):
        super().__init__(message)
        self.code = code

    def __str__(self) -> str:
        return repr(self)


__all__ = ["immutableprop"]


class immutableprop(property):
    _MESSAGE = "Property state cannot be mutated!!"

    def __init__(self, fget, *args) -> None:
        super().__init__(fget, self._set_error)

    def _set_error(self, _1, _2) -> None:
        raise RuntimeError(self._MESSAGE)

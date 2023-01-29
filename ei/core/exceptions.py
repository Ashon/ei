
class BaseError(RuntimeError):
    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {"".join(self.args)}'


class PreflightError(BaseError):
    pass


class WrongRegionError(BaseError):
    pass


class WrongAccountError(BaseError):
    pass


class ResourceNotfoundError(BaseError):
    pass

from typing import Optional


class Error(Exception):
    pass


class OperationError(Error):
    """ Custom class errors """

    def __init__(
        self,
        status: int,
        message: str,
        e: Optional[Exception] = None,
    ) -> None:
        """
        initialization class

        Args:
            status: status of error
            message: text of error
            e: thrown exception
        """
        self.status = status
        self.msg = f"{message}"
        if e is not None:
            self.msg += f"{e.__str__()}"

"""Custom exceptions classes for Flora."""
import json
from datetime import datetime as dt
from sys import exc_info
from typing import Any, Optional, Union


class FloraException(Exception):
    """Base exception for all Flora exceptions."""

    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        module: str = "model",
        datetime: Optional[Union[str, dt]] = None,
        user_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        data: Optional[Any] = None,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.module = module
        self.message = message
        if datetime is None:
            self.datetime = dt.now().isoformat()
        else:
            # Convert datetime to isoformat if it is not already
            if isinstance(datetime, dt):
                self.datetime = datetime.isoformat()
            else:
                self.datetime = datetime
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.data = data

        self.traceback = exc_info()

        super().__init__(str(self))

    def __str__(self) -> str:
        """Convert the exception to a JSON string,
        which is to be parsed by the error handler.

        All fields are in camelCase.

        Returns:
            str: JSON string
        """
        return json.dumps(
            {
                "errorCode": f"{self.module}/{self.error_code}",
                "statusCode": self.status_code,
                "module": self.module,
                "message": self.message,
                "datetime": self.datetime,
                "userId": self.user_id,
                "workspaceId": self.workspace_id,
                "data": self.data,
            }
        )

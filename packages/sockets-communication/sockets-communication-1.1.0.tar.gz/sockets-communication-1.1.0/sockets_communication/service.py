# service.py

import threading
import warnings
import time
import datetime as dt
from typing import Optional, Union

from represent import BaseModel

Number = Union[int, float]
Host = str
Port = Union[str, int]

__all__ = [
    "ServiceInterface"
]

class ServiceInterface(BaseModel):
    """The server object to control the communication ith multiple clients."""

    def __init__(self) -> None:
        """Defines the server datasets for clients and client commands."""

        self._timeout_process: Optional[threading.Thread] = None

        self._blocking = False
    # end __init__

    @property
    def blocking(self) -> bool:
        """
        Returns the value of te execution being blocking by the service loop.

        :return: The blocking value.
        """

        return self._blocking
    # end blocking

    def start_blocking(self) -> None:
        """Starts the blocking process."""

        if self.blocking:
            warnings.warn(f"Blocking process of {self} is already running.")

            return
        # end if

        self._blocking = True

        while self.blocking:
            time.sleep(0.005)
        # end while
    # end start_blocking

    @staticmethod
    def start_waiting(
            wait: Union[Number, dt.timedelta, dt.datetime]
    ) -> None:
        """
        Runs a waiting for the process.

        :param wait: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        if isinstance(wait, dt.datetime):
            wait = wait - dt.datetime.now()
        # end if

        if isinstance(wait, dt.timedelta):
            wait = wait.total_seconds()
        # end if

        if isinstance(wait, (int, float)):
            time.sleep(wait)
        # end if
    # end start_waiting

    def run(
            self,
            block: Optional[bool] = False,
            wait: Optional[Union[Number, dt.timedelta, dt.datetime]] = None,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None,
    ) -> None:
        """
        Runs the api service.

        :param block: The value to block the execution and wain for the service.
        :param wait: The waiting time.
        :param timeout: The start_timeout for the process.
        """

        if timeout:
            self.start_timeout(timeout)
        # end if

        if wait:
            self.start_waiting(wait)
        # end if

        if block:
            self.start_blocking()
        # end if
    # end run

    def start_timeout(
            self,
            duration: Union[Number, dt.timedelta, dt.datetime]
    ) -> None:
        """
        Waits to terminate the process.

        :param duration: The amount of seconds to wait before termination.
        """

        if isinstance(duration, dt.datetime):
            duration = duration - dt.datetime.now()
        # end if

        if isinstance(duration, dt.timedelta):
            duration = duration.total_seconds()
        # end if

        self._timeout_process = threading.Thread(
            target=lambda: (time.sleep(duration), self.terminate())
        )

        self._timeout_process.start()
    # end start_timeout

    def stop_blocking(self) -> None:
        """Stops the blocking process."""

        self._blocking = False
    # end stop_blocking

    def terminate(self) -> None:
        """Pauses the process of service."""

        self.stop_blocking()
    # end terminate
# end ServiceInterface
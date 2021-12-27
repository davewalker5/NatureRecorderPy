"""
This module defines a base class for data exchange helpers that complete on a background thread
"""

import threading
from typing import Optional


class DataExchangeHelperBase(threading.Thread):
    def __init__(self, action):
        """
        Initialiser

        :param action: Callable to perform the data exchange operation
        """
        threading.Thread.__init__(self)
        self._action = action
        self._exception = None

    def run(self, *args, **kwargs):
        """
        Import conservation status schemes and ratings from a CSV file on a background thread

        :param args: Variable positional arguments
        :param kwargs: Variable keyword arguments
        """
        try:
            self._action()
        except BaseException as e:
            # If we get an error during import, capture it. join(), below, then raises it in the calling
            # thread
            self._exception = e

    def join(self, timeout: Optional[float] = ...) -> None:
        """
        If we have an exception, raise it in the calling thread when joined
        """
        threading.Thread.join(self)
        if self._exception:
            raise self._exception

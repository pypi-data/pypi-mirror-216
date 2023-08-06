import inspect
import logging
import os
import sys
import warnings
from functools import lru_cache
from typing import Callable, Optional, Union

from .singleton import Singleton

LOG_FORMAT = "%(asctime)-23s  %(levelname)-8s  %(name)-32s  %(message)-160s  .(%(filename)s:%(lineno)d)"


class Logging(metaclass=Singleton):
    def __init__(self, stacklevel: int = 0):
        # Ensure the routing of warnings to the logger when using the logger
        logging.captureWarnings(True)

        def get_logger(name):
            return logging.getLogger().getChild(name)

        self.get_root_logger: Callable[[str], logging.Logger] = get_logger
        if sys.gettrace() is None:
            logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
        else:
            logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    def __fix_get_root_logger(self, x):
        """Quick fix to support 2 structures of root logger"""
        try:
            out = self.get_root_logger(x)
        except Exception:
            out = self.get_root_logger()
        return out

    def _get_logger(self, failsafe: bool = True, stack_level: int = 0):
        try:
            frame = inspect.stack()[2 + stack_level]
            mod = inspect.getmodule(frame[0])
            # return self.get_root_logger(mod.__package__)
            return self.__fix_get_root_logger(mod.__name__.split(".")[-1])
        except Exception as e:
            if failsafe is True:
                warnings.warn(
                    "There was an issue in accessing the desired logger - defaulting to a failsafe one"
                )
                return self.__fix_get_root_logger("Failsafe-log (preheat_open)")
            else:
                raise e

    def set_root_logger(self, func: Callable[[str], logging.Logger]):
        self.get_root_logger = func

    def set_level(self, level: Union[str, int]) -> None:
        logging.basicConfig(level=level, force=True)

    def critical(
        self,
        msg: str,
        exception: Optional[Exception] = None,
        stack_level: int = 0,
        *args,
        **kwargs,
    ) -> None:
        if exception is None:
            [
                self._get_logger(stack_level=stack_level).critical(
                    line, stacklevel=2 + stack_level, *args, **kwargs
                )
                for line in str(msg).split("\n")
            ]

        else:
            try:
                raise exception
            except Exception as e:
                [
                    self._get_logger(stack_level=stack_level).exception(
                        line, stacklevel=2 + stack_level, *args, **kwargs
                    )
                    for line in str(msg).split("\n")
                ]

    def error(
        self,
        msg: str,
        exception: Optional[Exception] = None,
        stack_level: int = 0,
        *args,
        **kwargs,
    ) -> None:
        if exception is None:
            [
                self._get_logger(stack_level=stack_level).error(
                    line, stacklevel=2 + stack_level, *args, **kwargs
                )
                for line in str(msg).split("\n")
            ]

        else:
            try:
                raise exception
            except Exception as e:
                [
                    self._get_logger(stack_level=stack_level).exception(
                        line, stacklevel=2 + stack_level, *args, **kwargs
                    )
                    for line in str(msg).split("\n")
                ]

    def warning(
        self, msg: Union[str, Warning], stack_level: int = 0, *args, **kwargs
    ) -> None:
        if isinstance(msg, Warning):
            warnings.warn(msg)
        else:
            [
                self._get_logger(stack_level=stack_level).warning(
                    line, stacklevel=2 + stack_level, *args, **kwargs
                )
                for line in str(msg).split("\n")
            ]

    def info(self, msg: str, stack_level: int = 0, *args, **kwargs) -> None:
        [
            self._get_logger(stack_level=stack_level).info(
                line, stacklevel=2 + stack_level, *args, **kwargs
            )
            for line in str(msg).split("\n")
        ]

    def debug(self, msg: str, stack_level: int = 0, *args, **kwargs) -> None:
        [
            self._get_logger(stack_level=stack_level).debug(
                line, stacklevel=2 + stack_level, *args, **kwargs
            )
            for line in str(msg).split("\n")
        ]


def logging_level(level: str) -> int:
    """
    Converts a string to a logging level

    :param level: logging level (debug, info, warning, error, critical)
    :type level:
    :return: logging level identifier (in logging package)
    :rtype:
    """
    if isinstance(level, str):
        str_level = level.lower()
        if str_level == "debug":
            log_level = logging.DEBUG
        elif str_level == "info":
            log_level = logging.INFO
        elif str_level == "warning":
            log_level = logging.WARNING
        elif str_level == "error":
            log_level = logging.ERROR
        elif str_level == "critical":
            log_level = logging.CRITICAL
        else:
            raise Exception(f"Illegal logging level ({level})")

        return log_level

    else:
        raise Exception("Only logging levels in string format are supported for now")


def set_logging_level(level: str) -> None:
    """
    Sets the logging level

    :param level: logging level (debug, info, warning, error, critical)
    :type level:
    """
    Logging().set_level(logging_level(level))


@lru_cache(maxsize=1)
def __profiling_log_file_path() -> Optional[str]:
    return os.environ.get("PREHEAT_OPEN_LOG_PROFILER")


@lru_cache(maxsize=1)
def write_log_to_profiling_file_is_active() -> bool:
    """
    Method to determine whether to enable the logging to a profiling file
    (enable by setting the environment variable "PREHEAT_OPEN_LOG_PROFILER")
    """
    v = __profiling_log_file_path()
    return v is not None


def write_log_to_profiling_file(message: str) -> None:
    """
    Method to write a line to the profiling file, which can be used to track which kind of I/O is used
    (enable by setting the environment variable "PREHEAT_OPEN_LOG_PROFILER")
    """
    if not write_log_to_profiling_file_is_active():
        return

    with open(__profiling_log_file_path(), "a") as f:
        f.write(message + "\n")

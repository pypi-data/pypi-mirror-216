"""
Managing minimalistic caching of data

The functions automatically take care of creating the folder structure to host the cache files, if needed.
"""


import os
import pickle
from datetime import datetime
from typing import Any, Optional

from preheat_open.logging import Logging


def __create_folder_if_needed(path: str) -> None:
    """
    Ensures that a given output folder (path) exists by creating it if it doesn't

    :param path: str
    :return: /
    """
    if os.path.isdir(path):
        return

    current_path = ""
    folders_in_path = path.split("/")
    for p_i in folders_in_path:
        current_path += f"{p_i}/"
        if (len(current_path) > 1) and (os.path.isdir(current_path) is False):
            Logging().info(f"Creating folder: {current_path}")
            os.mkdir(current_path)


def __cache_filename(
    id: str,
    path: str,
) -> str:
    if not path.endswith("/"):
        path = path + "/"
    __create_folder_if_needed(path)
    if id.endswith(".pkl"):
        out = f"{path}{id}"
    else:
        out = f"{path}{id}.pkl"
    return out


def save_to_cache(data: Any, id: str, path: str = ".cache/") -> None:
    """
    Save given data to an on-disk cache

    :param data: data to cache
    :param id: cache identifier
    :param path: path on which to save the data
    :return: /
    """
    filename = __cache_filename(id, path)
    Logging().debug(f"Caching data to {filename}")
    with open(filename, "wb") as file_id:
        try:
            pickle.dump(data, file=file_id)
        except Exception as e:
            Logging().warning(
                RuntimeWarning(f"Failed to cache to {filename} (exception: {e})")
            )


def load_from_cache(
    id: str,
    expiry_s: Optional[int] = None,
    path: str = ".cache/",
) -> tuple[Any, bool]:
    """
    Loads data from the on-disk cache.

    WARNING: this method loads data from a file using pickle, which may execute code at the time of loading.
        Make sure to load only files that you generated yourself or trust in order to avoid execution of malicious code.

    :param id: cache identifier
    :param expiry_s: acceptable lifetime of the cache (in s)
    :param path: path in which to cache the data
    :return: tuple of:
        data loaded from cache (or None if non-existent) and
        indicator of whether data was loaded
    """
    filename = __cache_filename(id, path)
    if os.path.exists(filename) is False:
        data_should_be_loaded = False
    else:
        if expiry_s is None:
            data_should_be_loaded = True
        elif os.path.getsize(filename) <= 0:
            # If the file is empty, skip the data loading
            data_should_be_loaded = False
        else:
            file_age_s = (datetime.now().timestamp()) - (os.path.getmtime(filename))
            if file_age_s <= expiry_s:
                data_should_be_loaded = True
            else:
                data_should_be_loaded = False
                os.remove(filename)

    data = None
    data_was_loaded = False

    if data_should_be_loaded is True:
        with open(filename, "rb") as file_id:
            try:
                Logging().debug(f"Loading data from cache in {filename}")
                data = pickle.load(file=file_id)
                data_was_loaded = True
            except Exception as e:
                Logging().warning(
                    RuntimeWarning(
                        f"Failed to load from cache in {filename} (exception: {e})"
                    )
                )

    return data, data_was_loaded


def delete_from_cache(id: str, path: str = ".cache/") -> None:
    """
    Deletes data from the on-disk cache

    :param id: cache identifier
    :param path: path in which to cache the data
    :return: /
    """

    filename = __cache_filename(id, path)
    if os.path.exists(filename) is True:
        Logging().debug(f"Deleting cache from {filename}")
        os.remove(filename)

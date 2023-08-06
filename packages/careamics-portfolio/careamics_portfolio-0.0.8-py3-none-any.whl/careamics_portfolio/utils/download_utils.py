from pathlib import Path
from typing import Optional, Union

import pooch
from pooch import Pooch


def get_registry_path() -> Path:
    """Get the path to the registry.txt file.

    Returns
    -------
    Path
        Path to the registry.txt file.
    """
    return Path(__file__).parent / "../registry/registry.txt"


def get_poochfolio(path: Optional[Union[str, Path]] = None) -> Pooch:
    """Create the pooch object for the whole portfolio.

    By default the files will be downloaded and cached in the user's
    cache folder and can be retrieved automatically without downloading
    the file anew (thanks pooch!).


    Attributes
    ----------
    path : Path
        Path to the folder in which to download the dataset. Defaults to None.

    Returns
    -------
    Pooch
        Pooch object for the whole portfolio.

    """
    if path is None:
        path = pooch.os_cache("portfolio")

    poochfolio = pooch.create(
        path=path,
        base_url="",
    )

    # Path to the registry.txt file
    poochfolio.load_registry(get_registry_path())

    return poochfolio

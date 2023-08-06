from pathlib import Path
from typing import Any, List, Optional, Union

from pooch import Unzip

from .utils import get_poochfolio


class PortfolioEntry:
    """Base class for portfolio entries.

    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        name (str): Name of the dataset.
        url (str): URL of the dataset.
        description (str): Description of the dataset.
        license (str): License of the dataset.
        citation (str): Citation to use when referring to the dataset.
        file_name (str): Name of the downloaded file.
        hash (str): SHA256 hash of the downloaded file.
        files (list[str]): List of files in the dataset.
        size (int): Size of the dataset in MB.
        tags (list[str]): List of tags associated to the dataset.
        is_zip (bool): Whether the dataset is a zip file.
    """

    def __init__(
        self,
        portfolio: str,
        name: str,
        url: str,
        description: str,
        license: str,
        citation: str,
        file_name: str,
        sha256: str,
        files: List[str],
        size: float,
        tags: List[str],
        is_zip: bool = True,
        **kwargs: str,
    ) -> None:
        self._portfolio = portfolio

        if " " in name:
            raise ValueError("Dataset name cannot contain spaces.")
        self._name = name

        self._url = url
        self._description = description
        self._license = license
        self._citation = citation
        self._file_name = file_name
        self._hash = sha256
        self._files = files
        self._size = size
        self._tags = tags
        self._is_zip = is_zip

    @property
    def portfolio(self) -> str:
        """Name of the portfolio the dataset belong to.

        Returns
        -------
        str
            Name of the portfolio the dataset belong to.
        """
        return self._portfolio

    @property
    def name(self) -> str:
        """Name of the dataset.

        Returns
        -------
        str
            Name of the dataset.
        """
        return self._name

    @property
    def url(self) -> str:
        """URL of the dataset.

        Returns
        -------
        str
            URL of the dataset.
        """
        return self._url

    @property
    def description(self) -> str:
        """Description of the dataset.

        Returns
        -------
        str
            Description of the dataset.
        """
        return self._description

    @property
    def license(self) -> str:
        """License of the dataset.

        Returns
        -------
        str
            License of the dataset.
        """
        return self._license

    @property
    def citation(self) -> str:
        """Citation to use when referring to the dataset.

        Returns
        -------
        str
            Citation to use when referring to the dataset.
        """
        return self._citation

    @property
    def file_name(self) -> str:
        """Name of the downloaded file.

        Returns
        -------
        str
            Name of the downloaded file.
        """
        return self._file_name

    @property
    def hash(self) -> str:
        """SHA256 hash of the downloaded file.

        Returns
        -------
        str
            SHA256 hash of the downloaded file.
        """
        return self._hash

    @property
    def files(self) -> List[str]:
        """Dictionary of files in the dataset.

        Returns
        -------
        dict[str, list]
            Dictionary of files in the dataset.
        """
        return self._files

    @property
    def size(self) -> float:
        """Size of the dataset in MB.

        Returns
        -------
        float
            Size of the dataset in MB.
        """
        return self._size

    @property
    def tags(self) -> List[str]:
        """List of tags associated to the dataset.

        Returns
        -------
        List[str]
            List of tags associated to the dataset.
        """
        return self._tags

    @property
    def is_zip(self) -> bool:
        """Whether the dataset is a zip file.

        Returns
        -------
        bool
            Whether the dataset is a zip file.
        """
        return self._is_zip

    def __str__(self) -> str:
        """Convert PortfolioEntry to a string.

        Returns
        -------
        str: A string containing the PortfolioEntry attributes.
        """
        return str(self.to_dict())

    def get_registry_name(self) -> str:
        """Return the name of the entry in the global registry.

        Returns
        -------
        str
            Name of the entry.
        """
        return self.portfolio + "-" + self.name

    def to_dict(self) -> dict:
        """Convert PortfolioEntry to a dictionary.

        Returns
        -------
            dict: A dictionary containing the PortfolioEntry attributes.
        """
        return {
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "license": self.license,
            "citation": self.citation,
            "file_name": self.file_name,
            "hash": self.hash,
            "files": self.files,
            "size": self.size,
            "tags": self.tags,
        }

    def download(
        self,
        path: Optional[Union[str, Path]] = None,
    ) -> Union[List[str], Any]:
        """Download dataset in the specified path.

        By default the files will be downloaded in the system's cache folder,
        and can be retrieved using this function without downloading the file
        anew (thanks pooch!).

        Parameters
        ----------
        path : str | Path
            Path to the folder in which to download the dataset. Defaults to
            None.

        Returns
        -------
        List[str]
            List of path(s) to the downloaded file(s).
        """
        poochfolio = get_poochfolio(path)

        # download data
        if self.is_zip:
            return poochfolio.fetch(
                fname=self.get_registry_name(),
                processor=Unzip(),
                progressbar=True,
            )
        else:
            return poochfolio.fetch(
                fname=self.get_registry_name(),
                progressbar=True,
            )

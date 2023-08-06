from __future__ import annotations

import json
from dataclasses import dataclass
from json import JSONEncoder
from pathlib import Path

from .denoiseg_datasets import (
    DENOISEG,
    DSB2018,
    MouseNuclei,
    NoiseLevel,
    SegFlywing,
)
from .denoising_datasets import (
    DENOISING,
    N2V_BSD68,
    N2V_RGB,
    N2V_SEM,
    Convallaria,
    Flywing,
)
from .portfolio_entry import PortfolioEntry
from .utils.download_utils import get_registry_path
from .utils.pale_blue_dot import PaleBlueDot
from .utils.pale_blue_dot_zip import PaleBlueDotZip


class IterablePortfolio:
    """Iterable portfolio class.

    Subclass this class and add PortfolioEntry objects as attributes.


    Attributes
    ----------
    _name : str
        Name of the portfolio.
    _datasets : List[PortfolioEntry]
        List of datasets in the portfolio.
    _current_index : int
    Current index of the iterator.
    """

    def __init__(self, name: str) -> None:
        self._name = name

        # create list of datasets
        datasets = []
        for dataset in vars(self).values():
            if isinstance(dataset, PortfolioEntry):
                datasets.append(dataset)

        # record datasets
        self._datasets = datasets
        self._current_index = 0

    def __iter__(self) -> IterablePortfolio:
        """Iterator method.

        Returns
        -------
        IterablePortfolio
            Iterator over the portfolio.
        """
        return self

    def __next__(self) -> PortfolioEntry:
        """Next method.

        Returns
        -------
        PortfolioEntry
            Next dataset in the portfolio.
        """
        if self._current_index < len(self._datasets):
            next_dataset = self._datasets[self._current_index]
            self._current_index += 1
            return next_dataset
        raise StopIteration("The iterator does not have any more elements.")

    @property
    def name(self) -> str:
        """Name of the portfolio.

        Returns
        -------
        str
            Name of the portfolio.
        """
        return self._name

    def list_datasets(self) -> list[str]:
        """List datasets in the portfolio using friendly names.

        The friendly names are the names of the portfolio entries, rather
        than that of the IterablePortfolio attributes.

        Returns
        -------
        list[str]
            List of datasets in the portfolio.
        """
        attributes = []

        # for each attribute
        for attribute in vars(self).values():
            if isinstance(attribute, PortfolioEntry):
                attributes.append(attribute.name)

        return attributes

    def as_dict(self) -> dict:
        """Dictionary representation of a portfolio.

        Used to serialize the class to json, with friendly names as entries.

        Returns
        -------
        dict[str]
            Dictionary representation of the DenoiSeg portfolio.
        """
        entries = {}

        # for each attribute
        for attribute in vars(self).values():
            # if the attribute is a PortfolioEntry
            if isinstance(attribute, PortfolioEntry):
                # add the attribute to the entries dictionary
                entries[attribute.name] = {
                    "URL": attribute.url,
                    "Description": attribute.description,
                    "Citation": attribute.citation,
                    "License": attribute.license,
                    "Hash": attribute.hash,
                    "File size": f"{attribute.size} MB",
                    "Tags": attribute.tags,
                }
        return entries

    def __str__(self) -> str:
        """String representation of a portfolio.

        Returns
        -------
        str
        String representation of a portfolio.
        """
        return f"{self.name} datasets: {self.list_datasets()}"


class ItarablePortfolioEncoder(JSONEncoder):
    """Portfolio encoder class."""

    def default(self, o: IterablePortfolio) -> dict[str, dict[str, str]]:
        """Default method for json export.

        Parameters
        ----------
        o : IterablePortfolio
            Portfolio to export.

        Returns
        -------
        dict[str, str]
            Dictionary representation of the portfolio.
        """
        return o.as_dict()


class DenoiSeg(IterablePortfolio):
    """An IterablePortfolio of DenoiSeg datasets.

    Attributes
    ----------
        DSB2018_n0 (DSB2018): DSB2018 dataset with noise level 0.
        DSB2018_n10 (DSB2018): DSB2018 dataset with noise level 10.
        DSB2018_n20 (DSB2018): DSB2018 dataset with noise level 20.
        Flywing_n0 (SegFlywing): Flywing dataset with noise level 0.
        Flywing_n10 (SegFlywing): Flywing dataset with noise level 10.
        Flywing_n20 (SegFlywing): Flywing dataset with noise level 20.
        MouseNuclei_n0 (MouseNuclei): MouseNuclei dataset with noise level 0.
        MouseNuclei_n10 (MouseNuclei): MouseNuclei dataset with noise level 10.
        MouseNuclei_n20 (MouseNuclei): MouseNuclei dataset with noise level 20.
    """

    def __init__(self) -> None:
        self._DSB2018_n0 = DSB2018(NoiseLevel.N0)
        self._DSB2018_n10 = DSB2018(NoiseLevel.N10)
        self._DSB2018_n20 = DSB2018(NoiseLevel.N20)
        self._SegFlywing_n0 = SegFlywing(NoiseLevel.N0)
        self._SegFlywing_n10 = SegFlywing(NoiseLevel.N10)
        self._SegFlywing_n20 = SegFlywing(NoiseLevel.N20)
        self._MouseNuclei_n0 = MouseNuclei(NoiseLevel.N0)
        self._MouseNuclei_n10 = MouseNuclei(NoiseLevel.N10)
        self._MouseNuclei_n20 = MouseNuclei(NoiseLevel.N20)

        super().__init__(DENOISEG)

    @property
    def DSB2018_n0(self) -> DSB2018:
        """DSB2018 dataset with noise level 0.

        Returns
        -------
        DSB2018
            DSB2018 dataset with noise level 0.
        """
        return self._DSB2018_n0

    @property
    def DSB2018_n10(self) -> DSB2018:
        """DSB2018 dataset with noise level 10.

        Returns
        -------
        DSB2018
            DSB2018 dataset with noise level 10.
        """
        return self._DSB2018_n10

    @property
    def DSB2018_n20(self) -> DSB2018:
        """DSB2018 dataset with noise level 20.

        Returns
        -------
        DSB2018
            DSB2018 dataset with noise level 20.
        """
        return self._DSB2018_n20

    @property
    def Flywing_n0(self) -> SegFlywing:
        """Flywing dataset with noise level 0.

        Returns
        -------
        SegFlywing
            Flywing dataset with noise level 0.
        """
        return self._SegFlywing_n0

    @property
    def Flywing_n10(self) -> SegFlywing:
        """Flywing dataset with noise level 10.

        Returns
        -------
        SegFlywing
            Flywing dataset with noise level 10.
        """
        return self._SegFlywing_n10

    @property
    def Flywing_n20(self) -> SegFlywing:
        """Flywing dataset with noise level 20.

        Returns
        -------
        SegFlywing
            Flywing dataset with noise level 20.
        """
        return self._SegFlywing_n20

    @property
    def MouseNuclei_n0(self) -> MouseNuclei:
        """MouseNuclei dataset with noise level 0.

        Returns
        -------
        MouseNuclei
            MouseNuclei dataset with noise level 0.
        """
        return self._MouseNuclei_n0

    @property
    def MouseNuclei_n10(self) -> MouseNuclei:
        """MouseNuclei dataset with noise level 10.

        Returns
        -------
        MouseNuclei
            MouseNuclei dataset with noise level 10.
        """
        return self._MouseNuclei_n10

    @property
    def MouseNuclei_n20(self) -> MouseNuclei:
        """MouseNuclei dataset with noise level 20.

        Returns
        -------
        MouseNuclei
            MouseNuclei dataset with noise level 20.
        """
        return self._MouseNuclei_n20


class Denoising(IterablePortfolio):
    """An IterablePortfolio of denoising datasets.

    Attributes
    ----------
    N2V_BSD68 (N2V_BSD68): BSD68 dataset.
    N2V_SEM (N2V_SEM): SEM dataset.
    N2V_RGB (N2V_RGB): RGB dataset.
    flywing (Flywing): Flywing dataset.
    Convallaria (Convallaria): Convallaria dataset.
    """

    def __init__(self) -> None:
        self._N2V_BSD68 = N2V_BSD68()
        self._N2V_SEM = N2V_SEM()
        self._N2V_RGB = N2V_RGB()
        self._flywing = Flywing()
        self._Convallaria = Convallaria()

        super().__init__(DENOISING)

    @property
    def N2V_BSD68(self) -> N2V_BSD68:
        """BSD68 dataset.

        Returns
        -------
        N2V_BSD68
            BSD68 dataset.
        """
        return self._N2V_BSD68

    @property
    def N2V_SEM(self) -> N2V_SEM:
        """SEM dataset.

        Returns
        -------
        N2V_SEM
            SEM dataset.
        """
        return self._N2V_SEM

    @property
    def N2V_RGB(self) -> N2V_RGB:
        """RGB dataset.

        Returns
        -------
        N2V_RGB
            RGB dataset.
        """
        return self._N2V_RGB

    @property
    def flywing(self) -> Flywing:
        """Flywing dataset.

        Returns
        -------
        Flywing
            Flywing dataset.
        """
        return self._flywing

    @property
    def Convallaria(self) -> Convallaria:
        """Convallaria dataset.

        Returns
        -------
        Convallaria
            Convallaria dataset.
        """
        return self._Convallaria


@dataclass
class PortfolioManager:
    """Portfolio of datasets.

    Attributes
    ----------
    denoising (Denoising): Denoising datasets.
    denoiseg (DenoiSeg): DenoiSeg datasets.
    """

    def __init__(self) -> None:
        self._denoising = Denoising()
        self._denoiseg = DenoiSeg()
        # self._segmentation = Segmentation()

    @property
    def denoising(self) -> Denoising:
        """Denoising datasets.

        Returns
        -------
        Denoising
            Denoising datasets.
        """
        return self._denoising

    @property
    def denoiseg(self) -> DenoiSeg:
        """DenoiSeg datasets.

        Returns
        -------
        DenoiSeg
            DenoiSeg datasets.
        """
        return self._denoiseg

    def __str__(self) -> str:
        """String representation of the portfolio.

        This method allows having a frendly representation of the portfolio as string.

        Returns
        -------
        str
            String representation of the portfolio.
        """
        return (
            f"Portfolio:\n"
            f"Denoising datasets: {self.denoising.list_datasets()}\n"
            f"DenoiSeg datasets: {self.denoiseg.list_datasets()}"
        )

    def as_dict(self) -> dict[str, IterablePortfolio]:
        """Portfolio as dictionary.

        This method is used during json serialization to maintain human readable
        keys.

        Returns
        -------
        dict[str, IterablePortfolio]
            Portfolio as dictionary.
        """
        attributes = {}

        for attribute in vars(self).values():
            if isinstance(attribute, IterablePortfolio):
                attributes[attribute.name] = attribute

        return attributes

    def to_json(self, path: str | Path) -> None:
        """Save portfolio to json file using the `as_dict` method.

        Parameters
        ----------
        path : str or Path
            Path to json file.
        """
        with open(path, "w") as f:
            json.dump(self.as_dict(), f, indent=4, cls=ItarablePortfolioEncoder)

    def to_registry(self, path: str | Path) -> None:
        """Save portfolio as registry (Pooch).

        See: https://www.fatiando.org/pooch/latest/registry-files.html

        Parameters
        ----------
        path : str or Path
            Path to json file.
        """
        portfolios = self.as_dict()
        with open(path, "w") as file:
            file.write("# Portfolio datasets - pooch registry\n")
            file.write("# Generated by running " "scripts/update_registry.py\n\n")

            # write each portfolio
            for key in portfolios.keys():
                file.write(f"# {key} \n")
                for entry in portfolios[key]:
                    file.write(
                        f"{entry.get_registry_name()} " f"{entry.hash} {entry.url}\n"
                    )
                file.write("\n")

            # add pale blue dot for testing purposes
            file.write("# Test sample\n")
            pale_blue_dot = PaleBlueDot()
            file.write(
                f"{pale_blue_dot.get_registry_name()} "
                f"{pale_blue_dot.hash} {pale_blue_dot.url}\n"
            )
            pale_blue_dot_zip = PaleBlueDotZip()
            file.write(
                f"{pale_blue_dot_zip.get_registry_name()} "
                f"{pale_blue_dot_zip.hash} {pale_blue_dot_zip.url}\n"
            )


def update_registry(path: str | Path | None = None) -> None:
    """Update the registry.txt file."""
    if path is None:
        path = get_registry_path()

    portfolio = PortfolioManager()
    portfolio.to_registry(path)

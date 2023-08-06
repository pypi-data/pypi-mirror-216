import pytest

from careamics_portfolio import PortfolioManager
from careamics_portfolio.denoiseg_datasets import NoiseLevel, NoisyObject
from careamics_portfolio.portfolio import PortfolioEntry

from .utils import (
    download_checker,
    portoflio_entry_checker,
    unique_hash_checker,
    unique_url_checker,
)

DATASETS = list(PortfolioManager().denoiseg)


def all_datasets_getters(portfolio: PortfolioManager):
    assert isinstance(portfolio.denoiseg.DSB2018_n0, PortfolioEntry)
    assert isinstance(portfolio.denoiseg.DSB2018_n10, PortfolioEntry)
    assert isinstance(portfolio.denoiseg.DSB2018_n20, PortfolioEntry)
    assert isinstance(portfolio.denoiseg.Flywing_n0, PortfolioEntry)
    assert isinstance(portfolio.denoiseg.Flywing_n10, PortfolioEntry)
    assert isinstance(portfolio.denoiseg.Flywing_n20, PortfolioEntry)
    assert isinstance(portfolio.denoiseg.MouseNuclei_n0, PortfolioEntry)
    assert isinstance(portfolio.denoiseg.MouseNuclei_n10, PortfolioEntry)
    assert isinstance(portfolio.denoiseg.MouseNuclei_n20, PortfolioEntry)


@pytest.mark.dataset
@pytest.mark.parametrize("dataset", DATASETS)
def test_datasets(tmp_path, dataset: PortfolioEntry):
    """Test that all DenoiSeg datasets download properly.

    This test also checks the files and size.

    Parameters
    ----------
    tmp_path : Path
        Path to temporary directory.
    dataset : Dataset
        Dataset object.
    """
    download_checker(tmp_path, dataset)


def test_unique_hashes(portfolio: PortfolioManager):
    """Test that all DenoiSeg dataset hashes are unique.

    Parameters
    ----------
    portfolio : Portfolio
        Portfolio object.
    """
    unique_hash_checker(portfolio.denoiseg)


def test_unique_urls(portfolio: PortfolioManager):
    """Test that all DenoiSeg dataset URLs are unique.

    Parameters
    ----------
    portfolio : Portfolio
        Portfolio object.
    """
    unique_url_checker(portfolio.denoiseg)


def test_no_empty_dataset_entry(portfolio: PortfolioManager):
    """Test that no DenoiSeg dataset entry is empty.

    Parameters
    ----------
    portfolio : Portfolio
        Portfolio object.
    """
    for entry in portfolio.denoiseg:
        portoflio_entry_checker(entry)


@pytest.mark.parametrize("noise_level", [NoiseLevel.N0, NoiseLevel.N10, NoiseLevel.N20])
def test_noisy_dataset(noise_level):
    """Test that the NoisyDataset class works properly."""
    noisy_object = NoisyObject(noise_level=noise_level)
    assert noisy_object.noise_level == noise_level

import pytest

from careamics_portfolio import PortfolioManager
from careamics_portfolio.portfolio_entry import PortfolioEntry

from .utils import (
    download_checker,
    portoflio_entry_checker,
    unique_hash_checker,
    unique_url_checker,
)

DATASETS = list(PortfolioManager().denoising)


def all_datasets_getters(portfolio: PortfolioManager):
    assert isinstance(portfolio.denoising.N2V_SEM, PortfolioEntry)
    assert isinstance(portfolio.denoising.N2V_BSD68, PortfolioEntry)
    assert isinstance(portfolio.denoising.N2V_RGB, PortfolioEntry)
    assert isinstance(portfolio.denoising.flywing, PortfolioEntry)
    assert isinstance(portfolio.denoising.Convallaria, PortfolioEntry)


@pytest.mark.dataset
@pytest.mark.parametrize("dataset", DATASETS)
def test_datasets(tmp_path, dataset: PortfolioEntry):
    """Test that all denoising datasets download properly.

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
    """Test that all denoising dataset hashes are unique.

    Parameters
    ----------
    portfolio : Portfolio
        Portfolio object.
    """
    unique_hash_checker(portfolio.denoising)


def test_unique_urls(portfolio: PortfolioManager):
    """Test that all denoising dataset URLs are unique.

    Parameters
    ----------
    portfolio : Portfolio
        Portfolio object.
    """
    unique_url_checker(portfolio.denoising)


def test_no_empty_dataset_entry(portfolio: PortfolioManager):
    """Test that no denoising dataset entry is empty.

    Parameters
    ----------
    portfolio : Portfolio
        Portfolio object.
    """
    for entry in portfolio.denoising:
        portoflio_entry_checker(entry)

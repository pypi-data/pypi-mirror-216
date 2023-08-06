import pytest

from careamics_portfolio import PortfolioManager
from careamics_portfolio.utils.pale_blue_dot import PaleBlueDot
from careamics_portfolio.utils.pale_blue_dot_zip import PaleBlueDotZip


@pytest.fixture
def pale_blue_dot() -> PaleBlueDot:
    """Fixture for the PaleBlueDot.

    Returns
    -------
    PaleBlueDot
        The PaleBlueDot picture.
    """
    return PaleBlueDot()


@pytest.fixture
def pale_blue_dot_zip() -> PaleBlueDotZip:
    """Fixture for the PaleBlueDot.

    Returns
    -------
    PaleBlueDot
        The PaleBlueDot picture.
    """
    return PaleBlueDotZip()


@pytest.fixture
def portfolio() -> PortfolioManager:
    """Fixture for the Portfolio.

    Returns
    -------
    Portfolio
        The Portfolio.
    """
    return PortfolioManager()

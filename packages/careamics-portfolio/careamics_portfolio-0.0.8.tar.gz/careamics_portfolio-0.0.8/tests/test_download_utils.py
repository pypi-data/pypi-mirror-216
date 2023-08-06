from careamics_portfolio import PortfolioManager
from careamics_portfolio.utils import get_poochfolio, get_registry_path


def test_get_pooch(portfolio: PortfolioManager):
    """Test that the get_pooch function instantiates
    pooch with the correct registry."""
    poochfolio = get_poochfolio()

    # count the number of portfolio entries
    portfolio_dict = portfolio.as_dict()
    count_entries = 0
    for key in portfolio_dict.keys():
        count_entries += len(portfolio_dict[key].list_datasets())

    assert len(poochfolio.registry) == count_entries + 2  # count test datasets


def test_get_registry_path():
    """Test that the path to the registry is correct."""
    assert get_registry_path().name == "registry.txt"
    assert get_registry_path().exists()

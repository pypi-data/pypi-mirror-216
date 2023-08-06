from pathlib import Path

import pytest

from careamics_portfolio.portfolio_entry import PortfolioEntry


def test_download(tmp_path, pale_blue_dot: PortfolioEntry):
    assert Path(pale_blue_dot.download(tmp_path)).exists()


def test_download_zip(tmp_path, pale_blue_dot_zip: PortfolioEntry):
    files = pale_blue_dot_zip.download(tmp_path)

    for file in files:
        assert Path(file).exists(), f"{file} does not exist."


def test_download_in_invalid_path(tmp_path, pale_blue_dot: PortfolioEntry):
    """Test that downloading to an invalid path raises an error."""
    file_name = "file.txt"
    with open(tmp_path / file_name, "w") as f:
        f.write("CATS ARE NICE.")

    with pytest.raises((NotADirectoryError, FileNotFoundError)):
        pale_blue_dot.download(tmp_path / file_name)


def test_change_entry(pale_blue_dot: PortfolioEntry):
    """Check that changing a PortfolioEntry member raises an error.

    Parameters
    ----------
    pale_blue_dot : PaleBlueDot
        Test PortfolioEntry.
    """
    # Verify that we can access the members
    pale_blue_dot.name
    pale_blue_dot.url
    pale_blue_dot.description
    pale_blue_dot.license
    pale_blue_dot.citation
    pale_blue_dot.file_name
    pale_blue_dot.hash
    pale_blue_dot.files

    # Check that changing members raises errors
    with pytest.raises(AttributeError):
        pale_blue_dot.name = ""

    with pytest.raises(AttributeError):
        pale_blue_dot.url = ""

    with pytest.raises(AttributeError):
        pale_blue_dot.description = ""

    with pytest.raises(AttributeError):
        pale_blue_dot.license = ""

    with pytest.raises(AttributeError):
        pale_blue_dot.citation = ""

    with pytest.raises(AttributeError):
        pale_blue_dot.file_name = ""

    with pytest.raises(AttributeError):
        pale_blue_dot.hash = ""

    with pytest.raises(AttributeError):
        pale_blue_dot.files = {}


def test_registry_name(pale_blue_dot: PortfolioEntry):
    """Test that the registry name is correct."""
    assert (
        pale_blue_dot.get_registry_name()
        == pale_blue_dot.portfolio + "-" + pale_blue_dot.name
    )


def test_name_with_space():
    with pytest.raises(ValueError):
        PortfolioEntry(
            name="name with space",
            url="url",
            portfolio="portfolio",
            description="description",
            license="license",
            citation="citation",
            file_name="file name",
            sha256="34973248736ygdw3",
            files=["dsada"],
            size=1,
            tags=["dsadas"],
        )


def test_entry_to_str(pale_blue_dot: PortfolioEntry):
    """Test the export to str and dict."""
    assert str(pale_blue_dot) == str(pale_blue_dot.to_dict())

import os
from pathlib import Path

import pytest

from careamics_portfolio.portfolio import IterablePortfolio
from careamics_portfolio.portfolio_entry import PortfolioEntry


def unique_url_checker(iter_portfolio: IterablePortfolio) -> None:
    """Check that all urls are unique."""
    urls = []
    for entry in iter_portfolio:
        # add to list of urls
        urls.append(entry.url)

    assert len(urls) == len(set(urls)), f"Duplicated urls in {iter_portfolio.name}."


def unique_hash_checker(iter_portfolio: IterablePortfolio) -> None:
    """Check that all hashes are unique."""
    hashes = []
    for entry in iter_portfolio:
        # add to list of hashes
        hashes.append(entry.hash)

    assert len(hashes) == len(
        set(hashes)
    ), f"Duplicated hashes in {iter_portfolio.name}."


def portoflio_entry_checker(entry: PortfolioEntry) -> None:
    """Check that the PortfolioEntry does not have null or empty fields,
    as well as a non-null size and at least one file."""
    assert entry.name is not None and entry.name != "", f"Invalid name in {entry}"
    assert entry.url is not None and entry.url != "", f"Invalid url in {entry}"
    assert entry.hash is not None and entry.hash != "", f"Invalid md5 hash in {entry}"
    assert (
        entry.description is not None and entry.description != ""
    ), f"Invalid description in {entry}"
    assert (
        entry.citation is not None and entry.citation != ""
    ), f"Invalid citation in {entry}"
    assert (
        entry.license is not None and entry.license != ""
    ), f"Invalid license in {entry}"
    assert (
        entry.file_name is not None and entry.file_name != ""
    ), f"Invalid file name in {entry}"
    assert entry.files is not None and len(entry.files) > 0, f"Invalid files in {entry}"
    assert entry.size is not None and entry.size > 0, f"Invalid size in {entry}"


def download_checker(path: Path, dataset: PortfolioEntry) -> None:
    """Test that the file can be downloaded and that all fields
    correspond to reality."""
    # download dataset
    files = dataset.download(path)

    # check that the zip file exists
    path_to_zip = path / dataset.get_registry_name()
    assert (
        path_to_zip.exists()
    ), f"{dataset.get_registry_name()} does not exist after download."

    # root folder where the downloaded files are
    if dataset.is_zip:
        folder_root = path / (dataset.get_registry_name() + ".unzip")
    else:
        folder_root = path

    # check that the files exist and are in the returned list
    # TODO: currently some files have hidden macOS files that need to be removed in the
    # future
    files_portfolio = [str(Path(folder_root, s)) for s in dataset.files]
    for file in files_portfolio:
        assert Path(file).exists(), f"{file} does not exist."
        assert file in files, f"{file} not in downloaded files."

    # check file size with a tolerance of 5% or 3MB
    file_size = os.path.getsize(path_to_zip) / 1024 / 1024  # MB
    abs_tolerance = max(0.05 * dataset.size, 3)
    assert dataset.size == pytest.approx(file_size, abs=abs_tolerance), (
        f"{dataset.name} has not the expected size "
        f"(expected {dataset.size}, got {file_size})."
    )

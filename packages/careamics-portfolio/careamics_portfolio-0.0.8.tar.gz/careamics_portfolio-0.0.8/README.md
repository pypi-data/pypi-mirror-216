<p align="center">
  <a href="https://careamics.github.io/">
    <img src="https://raw.githubusercontent.com/CAREamics/.github/main/profile/images/banner_careamics.png">
  </a>
</p>

# CAREamics Portfolio

[![License](https://img.shields.io/pypi/l/careamics-portfolio.svg?color=green)](https://github.com/CAREamics/careamics-portfolio/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/careamics-portfolio.svg?color=green)](https://pypi.org/project/careamics-portfolio)
[![Python Version](https://img.shields.io/pypi/pyversions/careamics-portfolio.svg?color=green)](https://python.org)
[![CI](https://github.com/CAREamics/careamics-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/CAREamics/careamics-portfolio/actions/workflows/ci.yml)
[![Datasets CI](https://github.com/CAREamics/careamics-portfolio/actions/workflows/datasets_ci.yml/badge.svg)](https://github.com/CAREamics/careamics-portfolio/actions/workflows/datasets_ci.yml)
[![codecov](https://codecov.io/gh/CAREamics/careamics-portfolio/branch/main/graph/badge.svg)](https://codecov.io/gh/CAREamics/careamics-portfolio)

A helper package based on [pooch](https://github.com/fatiando/pooch) allowing
downloading various example datasets used in publications by the Jug lab,
including data featured in N2V, P(P)N2V, DivNoising, HDN, EmbedSeg, etc.

The complete list of datasets can be found in 
[datasets.json](https://raw.githubusercontent.com/CAREamics/careamics-portfolio/main/datasets/datasets.json).

CAREamics-portfolio tooling was generated using [pydev-guide/pyrepo-copier](https://github.com/pydev-guide/pyrepo-copier).

## Installation

To install the portfolio in your conda environment, simply use `pip`:
```bash
$ pip install careamics-portfolio
```

## Usage

Follow the [example notebook](examples/example.ipynb) for details on how to use the package.

The portfolio can be instantiated as follow:

```python
from careamics_portfolio import PortfolioManager

portfolio = PortfolioManager()
```

You can explore the different datasets easily:
```python
print(portfolio)
print(portfolio.denoising)
print(portfolio.denoising.N2V_SEM)
```

Finally, you can download the dataset of your choice:
```python
from pathlib import Path

data_path = Path('data')

# to the path of your choice
portfolio.denoising.N2V_SEM.download(data_path)

# or to your system's cache
portfolio.denoising.N2V_SEM.download()
```

By default, if you do not pass `path` to the `download()` method, all datasets
will be saved in your system's cache. New queries to download will not cause
the files to be downloaded again (thanks pooch!!).

**Important**: if you download all datasets of interest using the same path, 
[pooch](https://github.com/fatiando/pooch) will maintain a regsitry of files
and you will not have to download them again!

## Add a dataset to the portfolio

There are a few steps to follow in order to add a new dataset to the repository:

:white_check_mark: 1 - Create a `PortfolioEntry` child class

:white_check_mark: 2 - Instantiate the portfolio entry in an `IterablePortfolio`

:white_check_mark: 3 - Update `registry.txt`

:white_check_mark: 4 - Make sure all tests pass


> Note: To run the tests, you will need to have `pytest` installed. You can
> create an environment with `careamics-portfolio` and `pytest` by running:
> ```bash
> pip install "careamics-portfolio[test]"
> ```

### 1 - Create a portfolio entry

To add a dataset, subclass a `PortfolioEntry` and enter the following information 
(preferably in one of the current categories, e.g. `denoising_datasets.py`):
```python
class MyDataset(PortfolioEntry):
    def __init__(self) -> None:
        super().__init__(
            portfolio="Denoising", # for instance
            name="MyDataset",
            url="https://url.to.myfile/MyFile.zip",
            file_name="MyFile.zip",
            hash="953a815333805a423b7342971289h10121263917019bd16cc3341", # sha256
            description="Description of the dataset.",
            license="CC-BY 3.0",
            citation="Citation of the dataset",
            files={
                "/folder/in/the/zip": ["file1.tif", "file2.tif"], # folder can be "."
            },
            size=13.0, # size in MB
            tags=["tag1", "tag2"],
            is_zip=True,
        )
```

To obtain sha256 hash of your file, you can run the following code and read out
the sha256 from the pooch prompt:
```python
import pooch

url = "https://url.to.myfile/MyFile.zip"
pooch.retrieve(url, known_hash=None)
```

Likewise, to get the size in MB of your file:
```python
import os

os.path.getsize(file_path) / 1024 / 1024
```


### 2 - Add the entry to a portfolio

Add the file class to one of the categories (e.g. denoising) in 
`portfolio.py`:
```python
class Denoising(IterablePortfolio):
    def __init__(self) -> None:
        self._N2V_BSD68 = N2V_BSD68()
        self._N2V_SEM = N2V_SEM()
        self._N2V_RGB = N2V_RGB()
        self._flywing = Flywing()

        # add your dataset as a private attribute
        self._myDataset = MyDataset()

        [...]

    # and add a public getter
    @property
    def MyDataset(self) -> MyDataset:
        return self._myDataset
```

### 3 - Update registry

Finally, update the registry by running the following pythons script:
```bash
python script/update_registry.py
```

or run:
```python
from careamics_portfolio import update_registry
update_registry()
```

The [datasets.json](https://raw.githubusercontent.com/CAREamics/careamics-portfolio/main/datasets/datasets.json)
file is updated using:
```bash
python script/update_json.py
```

### 4 - Verify that all tests pass

Verify that all tests pass, it can take a while:

```bash
pytest
```


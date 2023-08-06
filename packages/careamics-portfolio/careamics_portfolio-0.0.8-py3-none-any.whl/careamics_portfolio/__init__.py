"""microscopy_protfolio.

A helper package to download example datasets used in various publications and
deep-learning algorithms, including data featured in N2V, P(P)N2V, DivNoising, HDN,
EmbedSeg, etc.
"""
__all__ = [
    "PortfolioManager",
    "update_registry",
    "__author__",
    "__email__",
    "__version__",
]

from importlib.metadata import PackageNotFoundError, version

from .portfolio import PortfolioManager, update_registry

try:
    __version__ = version("microscopy-portfolio")
except PackageNotFoundError:
    __version__ = "uninstalled"
__author__ = "Joran Deschamps"
__email__ = "joran.deschamps@fht.org"

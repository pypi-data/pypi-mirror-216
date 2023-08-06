from enum import Enum

from .portfolio_entry import PortfolioEntry

DENOISEG = "denoiseg"


class NoiseLevel(str, Enum):
    """An IntEnum representing the noise level of a dataset.

    N0 corresponds to the noise-free version of the dataset, N10 and N20 to
    images corrupted with Gaussian noise with zero-mean and standard deviations
    of 10 and 20, respectively.
    """

    N0 = "0"
    N10 = "10"
    N20 = "20"


class NoisyObject:
    """A mixin class for datasets with different noise levels.

    Attributes
    ----------
    noise_level (NoiseLevel): Noise level of the dataset.
    """

    def __init__(self, noise_level: NoiseLevel = NoiseLevel.N0, **kwargs: str) -> None:
        self._noise_level = noise_level

    @property
    def noise_level(self) -> NoiseLevel:
        """Noise level of the dataset."""
        return self._noise_level


class DSB2018(PortfolioEntry, NoisyObject):
    """The 2018 Data Science Bowl dataset used by DenoiSeg.

    The dataset is available in three different noise levels: N0, N10 and N20.


    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        noise_level (NoiseLevel): Noise level of the dataset.
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

    def __init__(self, noise_level: NoiseLevel = NoiseLevel.N0) -> None:
        """Initialize a DSB2018 instance.

        Parameters
        ----------
        noise_level : NoiseLevel, optional
            Noise level of the dataset, by default NoiseLevel.N0
        """
        super().__init__(
            portfolio=DENOISEG,
            noise_level=noise_level,
            name=f"DSB2018_n{noise_level.value}",
            url=self._get_url(noise_level),
            file_name=f"DSB2018_n{noise_level.value}.zip",
            sha256=self._get_hash(noise_level),
            description="From the Kaggle 2018 Data Science Bowl challenge, the "
            "training and validation sets consist of 3800 and 670 patches "
            "respectively, while the test set counts 50 images.\n"
            "Original data: "
            "https://www.kaggle.com/competitions/data-science-bowl-2018/data",
            license="GPL-3.0",
            citation="Caicedo, J.C., Goodman, A., Karhohs, K.W. et al. Nucleus "
            "segmentation across imaging experiments: the 2018 Data Science "
            "Bowl. Nat Methods 16, 1247-1253 (2019). "
            "https://doi.org/10.1038/s41592-019-0612-7",
            files=[
                f"DSB2018_n{noise_level.value}/train/train_data.npz",
                f"DSB2018_n{noise_level.value}/test/test_data.npz",
            ],
            size=self._get_size(noise_level),
            tags=["denoising", "segmentation", "nuclei", "fluorescence"],
        )

    @staticmethod
    def _get_url(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "https://zenodo.org/record/5156969/files/DSB2018_n0.zip?download=1"
        elif noise == NoiseLevel.N10:
            return "https://zenodo.org/record/5156977/files/DSB2018_n10.zip?download=1"
        else:
            return "https://zenodo.org/record/5156983/files/DSB2018_n20.zip?download=1"

    @staticmethod
    def _get_hash(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "729d7683ccfa1ad437f666256b23e73b3b3b3da6a8e47bb37303f0c64376a299"
        elif noise == NoiseLevel.N10:
            return "a4cf731aa0652f8198275f8ce29fb98e0c76c391a96b6092d0792fe447e4103a"
        else:
            return "6a732a12bf18fecc590230b1cd4df5e32acfa1b35ef2fca42db811cb8277c67c"

    @staticmethod
    def _get_size(noise: NoiseLevel) -> float:
        if noise == NoiseLevel.N0:
            return 40.2
        elif noise == NoiseLevel.N10:
            return 366.0
        else:
            return 368.0


class SegFlywing(PortfolioEntry, NoisyObject):
    """Flywing dataset used by DenoiSeg.

    The dataset is available in three different noise levels: N0, N10 and N20.


    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        noise_level (NoiseLevel): Noise level of the dataset.
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

    def __init__(self, noise_level: NoiseLevel = NoiseLevel.N0) -> None:
        """Initialize a Flywing instance.

        Parameters
        ----------
        noise_level : NoiseLevel, optional
            Noise level of the dataset, by default NoiseLevel.N0
        """
        super().__init__(
            portfolio=DENOISEG,
            noise_level=noise_level,
            name=f"Flywing_n{noise_level.value}",
            url=self._get_url(noise_level),
            file_name=f"Flywing_n{noise_level.value}.zip",
            sha256=self._get_hash(noise_level),
            description="This dataset consist of 1428 training and 252 "
            "validation patches of a membrane labeled fly wing. The test set "
            "is comprised of 50 additional images.",
            license="CC BY-SA 4.0",
            citation="Buchholz, T.O., Prakash, M., Schmidt, D., Krull, A., Jug, "
            "F.: Denoiseg: joint denoising and segmentation. In: European "
            "Conference on Computer Vision (ECCV). pp. 324-337. Springer (2020) 8, 9",
            files=[
                f"Flywing_n{noise_level.value}/train/train_data.npz",
                f"Flywing_n{noise_level.value}/test/test_data.npz",
            ],
            size=self._get_size(noise_level),
            tags=["denoising", "segmentation", "membrane", "fluorescence"],
        )

    @staticmethod
    def _get_url(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "https://zenodo.org/record/5156991/files/Flywing_n0.zip?download=1"
        elif noise == NoiseLevel.N10:
            return "https://zenodo.org/record/5156993/files/Flywing_n10.zip?download=1"
        else:
            return "https://zenodo.org/record/5156995/files/Flywing_n20.zip?download=1"

    @staticmethod
    def _get_hash(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "3fb49ba44e7e3e20b4fc3c77754f1bbff7184af7f343f23653f258d50e5d5aca"
        elif noise == NoiseLevel.N10:
            return "c599981b0900e6b43f0a742f84a5fde664373600dc5334f537b61a76a7be2a3c"
        else:
            return "604b3a3a081eaa57ee25d708bc9b76b85d05235ba09d7c2b25b171e201ea966f"

    @staticmethod
    def _get_size(noise: NoiseLevel) -> float:
        if noise == NoiseLevel.N0:
            return 47.0
        elif noise == NoiseLevel.N10:
            return 282.0
        else:
            return 293.0


class MouseNuclei(PortfolioEntry, NoisyObject):
    """Mouse nuclei dataset used by DenoiSeg.

    The dataset is available in three different noise levels: N0, N10 and N20.


    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        noise_level (NoiseLevel): Noise level of the dataset.
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

    def __init__(self, noise_level: NoiseLevel = NoiseLevel.N0) -> None:
        """Initialize a MouseNuclei instance.

        Parameters
        ----------
        noise_level : NoiseLevel, optional
            Noise level of the dataset, by default NoiseLevel.N0
        """
        super().__init__(
            portfolio=DENOISEG,
            noise_level=noise_level,
            name=f"MouseNuclei_n{noise_level.value}",
            url=self._get_url(noise_level),
            file_name=f"MouseNuclei_n{noise_level.value}.zip",
            sha256=self._get_hash(noise_level),
            description="A dataset depicting diverse and non-uniformly "
            "clustered nuclei in the mouse skull, consisting of 908 training "
            "and 160 validation patches. The test set counts 67 additional images",
            license="CC BY-SA 4.0",
            citation="Buchholz, T.O., Prakash, M., Schmidt, D., Krull, A., Jug, "
            "F.: Denoiseg: joint denoising and segmentation. In: European "
            "Conference on Computer Vision (ECCV). pp. 324-337. Springer (2020) 8, 9",
            files=[
                f"Mouse_n{noise_level.value}/train/train_data.npz",
                f"Mouse_n{noise_level.value}/test/test_data.npz",
            ],
            size=self._get_size(noise_level),
            tags=["denoising", "segmentation", "nuclei", "fluorescence"],
        )

    @staticmethod
    def _get_url(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "https://zenodo.org/record/5157001/files/Mouse_n0.zip?download=1"
        elif noise == NoiseLevel.N10:
            return "https://zenodo.org/record/5157003/files/Mouse_n10.zip?download=1"
        else:
            return "https://zenodo.org/record/5157008/files/Mouse_n20.zip?download=1"

    @staticmethod
    def _get_hash(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "5d6fd2fc23ab991a8fde4bd0ec5e9fc9299f9a9ddc2a8acb7095f9b02ff3c9d7"
        elif noise == NoiseLevel.N10:
            return "de634496e3e46a4887907b713fe6f575e410c3006046054bce67ef9398523c2c"
        else:
            return "d3d1bf8c89bb97a673a0791874e5b75a6a516ccaaeece0244b4e1e0afe7ab3ec"

    @staticmethod
    def _get_size(noise: NoiseLevel) -> float:
        if noise == NoiseLevel.N0:
            return 12.4
        elif noise == NoiseLevel.N10:
            return 161.0
        else:
            return 160.0

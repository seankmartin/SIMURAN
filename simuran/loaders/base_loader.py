"""The base loading class in SIMURAN."""

from abc import ABC, abstractmethod


class BaseLoader(ABC):
    """
    This abstract class defines the layout of a SIMURAN loader.

    The abstract methods load_signal, load_single_unit,
    load_spatial, and auto_fname_extraction
    must be defined by subclasses.

    Attributes
    ----------
    signal : simuran.base_signal.BaseSignal
        The last loaded signal object.
    spatial : simuran.spatial.Spatial
        The last loaded spatial object.
    single_unit : simuran.single_unit.SingleUnit
        The last loaded single unit object.
    source_filenames : dict
        A dictionary of filenames used for data loading.
    load_params : dict
        Parameters to pass to the loader function.

    """

    def __init__(self, load_params={}):
        """See help(BaseLoader)."""
        self.signal = None
        self.spatial = None
        self.single_unit = None
        self.source_filenames = {}
        self.load_params = load_params
        super().__init__()

    @abstractmethod
    def load_signal(self, *args, **kwargs):
        """
        Load a signal object from args and kwargs.

        Returns
        -------
        dict
            The keys of this dictionary are saved as attributes
            in simuran.signal.BaseSignal.load()

        """
        pass

    @abstractmethod
    def load_single_unit(self, *args, **kwargs):
        """
        Load a single unit object from args and kwargs.

        Returns
        -------
        dict
            The keys of this dictionary are saved as attributes
            in simuran.single_unit.SingleUnit.load()

        """
        pass

    @abstractmethod
    def load_spatial(self, *args, **kwargs):
        """
        Load spatial data object from args and kwargs.

        Returns
        -------
        dict
            The keys of this dictionary are saved as attributes
            in simuran.spatial.Spatial.load()

        """
        pass

    @abstractmethod
    def auto_fname_extraction(self, basefname, **kwargs):
        """
        Return the filenames that would be involved in loading basefname.

        For example, basefname could be an Axona .set file,
        and auto_fname_extraction would pick up all related recording files
        that are related to this .set file.

        Parameters
        ----------
        basefname : str
            The base name to use for auto extraction of filenames.
            For example, this could be a directory, a filename, etc.

        Returns
        -------
        fnames : dict
            A dictionary listing the filenames involved in loading.
        base : str
            The base file name, this could be basefname or a modified version.

        """
        pass

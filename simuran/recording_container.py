"""This module provides a container for multiple recording objects."""

import os
from copy import deepcopy

from simuran.containers import AbstractContainer
from simuran.recording import Recording
from skm_pyutils.py_path import get_all_files_in_dir


class RecordingContainer(AbstractContainer):

    def __init__(self, load_on_fly=True, **kwargs):
        super().__init__()
        self.load_on_fly = load_on_fly
        self.last_loaded = Recording()
        self.last_loaded_idx = None
        self.base_dir = None

    def auto_setup(
            self, start_dir, param_name="simuran_params.py",
            recursive=True, re_filter=None, subset=None):
        fnames = get_all_files_in_dir(
            start_dir, ext=".py", return_absolute=True,
            recursive=recursive, case_sensitive_ext=True,
            re_filter=re_filter)
        return self.setup(fnames, start_dir, param_name=param_name)

    def setup(self, filenames, start_dir, param_name="simuran_params.py"):
        param_files = []
        for fname in filenames:
            if os.path.basename(fname) == param_name:
                param_files.append(fname)
        should_load = not self.load_on_fly
        out_str_load = "Loading" if should_load else "Parsing"
        for i, param_file in enumerate(param_files):
            print("{} recording {} of {} at {}".format(
                out_str_load, i + 1, len(param_files), param_file))
            recording = Recording(
                param_file=param_file, load=should_load)
            if not recording.valid:
                print("Last recording was invalid, not adding to container")
            else:
                self.append(recording)
        self.base_dir = start_dir
        return param_files

    def get(self, idx):
        """This loads the data if not loaded."""
        if self.load_on_fly:
            if self.last_loaded_idx != idx:
                self.last_loaded = deepcopy(self[idx])
                self.last_loaded.load()
                self.last_loaded_idx = idx
            return self.last_loaded
        else:
            return self[idx]

    def get_results(self, idx):
        return self.data_from_attr_list([("results", None)], idx=idx)

    def subsample(self, idx_list=None, interactive=False, prop=None):
        if prop is None:
            prop = "source_file"
        return super().subsample(idx_list, interactive, prop)

    def _create_new(self, params):
        recording = Recording(params=params)
        return recording

    def __repr__(self):
        s_files = "\n".join([r.source_file for r in self])
        return "{} with {} elements picked from {}:\n{}".format(
            self.__class__.__name__, len(self), self.base_dir,
            s_files)
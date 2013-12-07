#
# Base class for scanners and analyzers.
#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging, scanned_datadir

import sos_analyzer.compat as SC
import sos_analyzer.utils as SU
import glob
import os
import os.path
import re
import sys


DICT_MZERO = dict()


class Runnable(object):

    name = "runnable"
    enabled = False

    def __init__(self, name=None, **kwargs):
        """
        :param name: Object's name
        """
        if name is not None:
            self.name = name

        for k, v in SC.iteritems(kwargs):
            if v is not None:
                setattr(self, k, v)

    def run(self):
        raise NotImplementedError("Child class must implement this!")


class RunnableWithConfig(Runnable):

    name = "runnable_with_config"
    conf = DICT_MZERO
    enabled = True

    def __init__(self, name=None, conf=None, **kwargs):
        """
        :param name: Object's name
        :param conf: A maybe nested dict holding object's configurations
        """
        super(RunnableWithConfig, self).__init__(name, **kwargs)

        if conf is not None and isinstance(conf, dict):
            self.conf = conf.get(self.name, DICT_MZERO)

        if self.getconf("disabled", False) or \
           not self.getconf("enabled", True):
            self.enabled = False

    def getconf(self, key, fallback=None, key_sep='.'):
        """
        :param key: Key to get configuration
        :param fallback: Fallback value if the value for given key is not found
        :param key_sep: Separator char to represents hierarchized configuraion
        """
        return SU.dic_get_recur(self.conf, key, fallback, key_sep)


class RunnableWithIO(RunnableWithConfig):

    name = "runnable_with_io"
    inputs_dir = os.path.sep  # '/' (root)
    inputs = []
    outputs_dir = "/tmp/outputs"

    def __init__(self, inputs_dir=None, inputs=None, outputs_dir=None,
                 name=None, conf=None, **kwargs):
        """
        :param inputs_dir: Path to dir holding inputs
        :param inputs: List of filename or path to input files, or glob pattern
            of filename or path to input files or None;
            ex. ["a/b.txt", "c.txt"], "a/b/*.yml"
        :param name: Object's name
        :param conf: A maybe nested dict holding object's configurations
        """
        super(Runnable, self).__init__(name, conf, inputs_dir=inputs_dir,
                                       inputs=inputs, outputs_dir=outputs_dir,
                                       **kwargs)
        self.input_paths = [self._compute_input_path(input) for input
                            in self.inputs]

    def _compute_input_path(self, input):
        """
        :param input: Input filename or path to input file
        :return: Path to output file
        """
        return os.path.join(self.inputs_dir, input)

    def _compute_output_path(self, input):
        """
        NOTE: Child class should override this method.

        :param input: Input filename or path to input file
        :return: Path to output file
        """
        return os.path.join(self.outputs_dir, self.input)

# vim:sw=4:ts=4:et:
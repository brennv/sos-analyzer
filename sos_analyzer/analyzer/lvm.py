#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import sos_analyzer.analyzer.base as Base


def find_lvm_device_filter(workdir, input="etc/lvm/lvm.conf.json"):
    """
    :see: ``sos_analyzer.scanner.etc_lvm_lvm_conf``
    """
    data = Base.load_scanned_data(workdir, input)
    if data:
        for section in data:
            if section["title"] == "devices":
                return section["values"].get("filter", [])


class Analyzer(Base.Analyzer):

    name = "lvm"

    def analyze(self, *args, **kwargs):
        return dict(lvm_filters=find_lvm_device_filter(self.workdir), )

# vim:sw=4:ts=4:et:

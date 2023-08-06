"""Rasterio-backed Zarr storage."""

# cython: c_string_type=unicode, c_string_encoding=utf8

include "gdal.pxi"

from collections.abc import MutableMapping
import itertools
import logging

from rasterio._path import _parse_path

from rasterio._io cimport DatasetReaderBase

log = logging.getLogger(__name__)


class GDALStore(MutableMapping):

    def __init__(self, dataset, path="/"):
        self.dataset = dataset
        self.path = path
        cdef GDALDatasetH hds = (<DatasetReaderBase?>self.dataset).handle()
        cdef GDALGroupH hroot = GDALDatasetGetRootGroup(hds)
        cdef GDALGroupH hgroup = NULL

        if self.path == "/":
            hgroup = hroot
        else:
            hgroup = GDALGroupOpenGroupFromFullname(hroot, self.path.encode("utf-8"), NULL)
            GDALGroupRelease(hroot)

        cdef char **names = NULL

        names = GDALGroupGetGroupNames(hgroup, NULL)

        log.debug("Number of groups in group: %r", CSLCount(names))

        self._group_keys = [names[i].decode("utf-8") for i in range(CSLCount(names))]

        CPLFree(names)

        names = GDALGroupGetMDArrayNames(hgroup, NULL)

        log.debug("Number of arrays in group: %r", CSLCount(names))

        self._array_keys = [names[i].decode("utf-8") for i in range(CSLCount(names))]

        CPLFree(names)

        GDALGroupRelease(hgroup)

    def __getitem__(self, key):
        if key in self._group_keys:
            return GDALStore(self.dataset, path="/".join([self.path.rstrip("/"), key]))
        elif key in self._array_keys:
            raise NotImplemented

    def __setitem__(self, key, val):
        pass

    def __delitem__(self, key, val):
        pass

    def __len__(self):
        return len(self._group_keys) + len(self._array_keys)

    def __iter__(self):
        return itertools.chain(self._group_keys, self._array_keys)

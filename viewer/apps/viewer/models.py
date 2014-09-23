import glob
import os

from django.conf import settings
from django.utils.functional import cached_property


class Node(object):

    def __init__(self, path, parent=None, count=1):
        self.parent = parent
        if self.parent:
            self.id = parent.id * 100 + count
        else:
            self.id = count
        self._path = path
        self._is_dir = os.path.isdir(self.path)

    @property
    def path(self):
        return self._path

    @cached_property
    def name(self):
        if self.is_dir():
            if self.parent:
                return os.path.relpath(self.path, self.parent.path)
            return self.path
        return os.path.basename(self.path)

    @cached_property
    def children(self):
        path = os.path.join(self._path, '*')
        return [Node(path, parent=self, count=i) for i, path in enumerate(glob.glob(path), 1)]

    @property
    def url_path(self):
        return os.path.relpath(self.path, settings.DATA_DIR)

    def is_dir(self):
        return self._is_dir

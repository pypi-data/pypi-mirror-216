"""
Task Storage.

Saving Tasks on different Storages (Filesystem, S3 buckets, databases, etc)
"""

from .filesystem import FileTaskStorage
from .database import DatabaseTaskStorage
from .row import RowTaskStorage
from .github import GitTaskStorage

__all__ = ['FileTaskStorage', 'DatabaseTaskStorage', 'RowTaskStorage', 'GitTaskStorage']

import io
import os
import google.auth
import gcsfs
from xia_storer import IOStorer


class GcsStorer(IOStorer):
    """Google Cloud Platform Based Storer
    """
    store_types = ['gcs']
    path_separator = "/"
    project_id = google.auth.default()[1]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'fs' in kwargs:
            if not isinstance(kwargs['fs'], gcsfs.GCSFileSystem):
                raise TypeError("GCSStorer Must have GCS based Filesystem")
            self.fs = kwargs['fs']
        else:
            self.fs = gcsfs.GCSFileSystem(**kwargs)

    @classmethod
    def get_data_path(cls, xia_id: str, topic_id: str, table_id: str, start_seq: str) -> str:
        """A xia_id should be a bucket

        Data is then organized by : topic_id, sysid, db, schema, table_name, start_seq
        """
        root = 'gs://' + cls.project_id + "-insight-data"
        table_id = '/'.join("_" if not item else item for item in table_id.split("."))
        return '/'.join([root, xia_id, topic_id, table_id, start_seq])

    def exists(self, location: str):
        return self.fs.exists(location)

    def walk_file(self, root_path):
        for root, dirs, files in self.fs.walk(root_path, topdown=False):
            for name in files:
                yield self.join(root, name)

    def join(self, *args):
        return '/'.join([item for item in args])

    def read(self, location: str) -> bytes:
        with self.fs.open(location, 'rb') as fp:
            return fp.read()

    def write(self, data_or_io, location: str) -> str:
        if isinstance(data_or_io, io.IOBase):
            with self.fs.open(location, 'wb') as fp:
                data_or_io.seek(0)
                chunk = data_or_io.read(2 ** 20)
                while chunk:
                    fp.write(chunk)
                    chunk = data_or_io.read(2 ** 20)
        elif isinstance(data_or_io, bytes):
            with self.fs.open(location, 'wb') as fp:
                fp.write(data_or_io)
        return location

    def remove(self, location: str) -> bool:
        if self.fs.exists(location):
            self.fs.rm(location)
            return True
        else:
            return True

    def mkdir(self, path: str):
        pass

    def get_io_stream(self, location: str):
        with self.fs.open(location, 'rb') as fp:
            yield fp

    def get_io_wb_stream(self, location: str):
        with self.fs.open(location, 'wb') as fp:
            yield fp

    def get_file_size(self, location: str) -> int:
        file_info = self.fs.info(location)
        return file_info.get("size") if file_info else None

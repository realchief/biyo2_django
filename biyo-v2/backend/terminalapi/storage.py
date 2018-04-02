import os
import errno

from django.core.files.storage import Storage
from django.utils._os import safe_join, abspathu
from django.core.files.move import file_move_safe
from django.core.files import locks, File
from django.core.exceptions import SuspiciousFileOperation
from django.utils.six.moves.urllib.parse import urljoin
from django.utils.encoding import filepath_to_uri


from django.conf import settings


class InstallerStorage(Storage):
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.STORAGE_ROOT
        self.base_location = location
        self.location = abspathu(self.base_location)
        if base_url is None:
            base_url = settings.STORAGE_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        return File(open(self.path(name), mode))

    def _save(self, name, content):
        full_path = self.path(name)

        # Create any intermediate directories that do not exist.
        # Note that there is a race between os.path.exists and os.makedirs:
        # if os.makedirs fails with EEXIST, the directory was created
        # concurrently, and we can continue normally. Refs #16082.
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        if not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)

        # There's a potential race condition between get_available_name and
        # saving the file; it's possible that two threads might return the
        # same name, at which point all sorts of fun happens. So we need to
        # try to create the file, but if it already exists we have to go back
        # to get_available_name() and try again.

        while True:
            try:
                # This file has a file path that we can move.
                if hasattr(content, 'temporary_file_path'):
                    file_move_safe(content.temporary_file_path(), full_path)
                    content.close()

                # This is a normal uploadedfile that we can stream.
                else:
                    # This fun binary flag incantation makes os.open throw an
                    # OSError if the file already exists before we open it.
                    flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                             getattr(os, 'O_BINARY', 0))
                    # The current umask value is masked out by os.open!
                    fd = os.open(full_path, flags, 0o666)
                    _file = None
                    try:
                        locks.lock(fd, locks.LOCK_EX)
                        for chunk in content.chunks():
                            if _file is None:
                                mode = 'wb' if isinstance(chunk, bytes) else 'wt'
                                _file = os.fdopen(fd, mode)
                            _file.write(chunk)
                    finally:
                        locks.unlock(fd)
                        if _file is not None:
                            _file.close()
                        else:
                            os.close(fd)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    # Ooops, the file exists. We need a new file name.
                    name = self.get_available_name(name)
                    full_path = self.path(name)
                else:
                    raise
            else:
                # OK, the file save worked. Break out of the loop.
                break

        #if settings.FILE_UPLOAD_PERMISSIONS is not None:
        #    os.chmod(full_path, settings.FILE_UPLOAD_PERMISSIONS)

        return name

    def delete(self, name):
        assert name, "The name argument is not allowed to be empty."
        name = self.path(name)
        # If the file exists, delete it from the filesystem.
        # Note that there is a race between os.path.exists and os.remove:
        # if os.remove fails with ENOENT, the file was removed
        # concurrently, and we can continue normally.
        if os.path.exists(name):
            try:
                os.remove(name)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

    def exists(self, name):
        return os.path.exists(self.path(name))

    def path(self, name):
        try:
            path = safe_join(self.location, name)
        except ValueError:

            raise SuspiciousFileOperation("Attempted access to '%s' denied." % name)
        return os.path.normpath(path)

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        split_name = name.split('/')
        return self.base_url + split_name[-1]
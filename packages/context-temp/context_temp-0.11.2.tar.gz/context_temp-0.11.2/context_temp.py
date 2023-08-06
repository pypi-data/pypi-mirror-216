__version__ = '0.11.2'

import contextlib, os, shutil, tempfile

# =============================================================================
# Context Managers
# =============================================================================

@contextlib.contextmanager
def temp_directory(path=None):
    """This ``Context Manager`` creates a temporary directory and yields its
    path.  Upon exit the directory is removed.

    :param path: optional path for the creation of the directory, otherwise
        defaults to operating system's default temp file location

    Example:

    .. code-block:: python

        with temp_directory() as td:
            filename = os.path.join(td, 'foo.txt')
            with open(filename, 'w') as f:
                f.write('stuff')

        # got here? => td is now gone, foo.txt is gone too
    """
    tempdir = tempfile.mkdtemp(dir=path)
    try:
        yield tempdir
    finally:
        shutil.rmtree(tempdir)


@contextlib.contextmanager
def temp_file(path=None):
    """This ``Context Manager`` creates a temporary file which is readable and
    writable by the current user and yields its path.  Once the ``Context``
    exits, the file is removed.

    :param path: optional path for the creation of the file, otherwise
        defaults to operating system's default temp file location

    Example:

    .. code-block:: python

        with temp_file() as filename:
            with open(filename, 'w') as f:
                f.write('stuff')
                
        # got here? => file called "filename" is now gone
    """
    _, filename = tempfile.mkstemp(dir=path)
    try:
        yield filename
    finally:
        os.remove(filename)

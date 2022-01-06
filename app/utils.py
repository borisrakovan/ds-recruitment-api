

def safe_makedir(path):
    """Make a directory if it doesn't exist, handling concurrent creation."""
    import os
    import errno
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
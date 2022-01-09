import typing as t


def safe_make_dir(path: str) -> None:
    """Make a directory if it doesn't exist, handling concurrent creation."""
    import os
    import errno
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def update_object_from_dict(object_to_update: object,
                            dict_with_changes: dict[str, t.Any],
                            *,
                            skip_non_null: bool = False) -> bool:
    """
    Sets values from dict to object fields if they differ from original ones.
    Skips fields with value already set if skip_non_null is True.
    Returns True if any field changed, False otherwise.
    """
    object_field_updated = False
    for key, value in dict_with_changes.items():
        object_attr = getattr(object_to_update, key)
        if (object_attr is not None and skip_non_null) \
                or object_attr == value:
            continue
        setattr(object_to_update, key, value)
        object_field_updated = True
    return object_field_updated

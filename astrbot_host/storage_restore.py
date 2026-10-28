"""Apply an already staged storage restore before opening the runtime."""

from companion_v2.storage.backup import PENDING_FILENAME, apply_pending, current_schema_version


def apply_staged_restore(data_root, *, installation_id: str, backup_directory=None) -> dict:
    """Apply a staged restore before the store is opened. No live connection exists.

    This is called from the host's assembly path before ``StorageRuntime.open``,
    which is the only moment the database file can be replaced without orphaning
    the shared connection. It reads the data root's current schema revision from
    the file itself, because the runtime is not available yet. Errors come back as
    a plain document rather than raising, so a failed restore leaves the original
    data root in place and start-up can continue.
    """
    from pathlib import Path
    root = Path(data_root)
    if not (root / PENDING_FILENAME).is_file():
        return {"applied": False, "reason": "no_pending_restore"}
    schema_version = current_schema_version(root)
    if schema_version is None:
        return {"applied": False, "reason": "backup_store_unreadable"}
    return apply_pending(root, installation_id=installation_id, schema_version=schema_version,
                         backup_directory=backup_directory)

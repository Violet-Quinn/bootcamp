import os
import shutil
import tempfile

def atomic_move(src: str, dst: str) -> None:
    """
    Atomically move a file from src to dst.
    Uses os.rename or shutil.move internally.
    """
    if not os.path.isfile(src):
        raise FileNotFoundError(f"Source file not found: {src}")
    dst_dir = os.path.dirname(dst)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)

    # Use os.rename on same filesystem, fallback to shutil.move
    try:
        os.rename(src, dst)
    except OSError:
        shutil.move(src, dst)

def timestamp_now() -> str:
    """
    Returns current UTC timestamp in ISO format.
    """
    import datetime
    return datetime.datetime.utcnow().isoformat() + "Z"

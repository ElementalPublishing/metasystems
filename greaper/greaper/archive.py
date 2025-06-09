import zipfile
import tarfile
import gzip
import bz2
import lzma
import rarfile  # pip install rarfile
import py7zr    # pip install py7zr
from pathlib import Path
import io

# Add more extensions as needed
ARCHIVE_EXTENSIONS = {
    ".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".lzma", ".7z", ".rar",
    ".whl", ".egg", ".jar", ".nupkg", ".tar.gz", ".tar.bz2", ".tar.xz"
}

def is_archive(filename):
    ext = Path(filename).suffix.lower()
    # Support double extensions like .tar.gz
    name = str(filename).lower()
    return (
        ext in ARCHIVE_EXTENSIONS or
        any(name.endswith(e) for e in ARCHIVE_EXTENSIONS)
    )

def list_archive_files(archive_path, _depth=0, _max_depth=3):
    """
    Returns a list of file names inside the archive.
    Supports nested archives up to _max_depth.
    """
    if _depth > _max_depth:
        return []
    archive_path = str(archive_path)
    files = []
    try:
        if archive_path.endswith((".zip", ".whl", ".egg", ".jar", ".nupkg")):
            with zipfile.ZipFile(archive_path) as z:
                for f in z.namelist():
                    if not f.endswith("/"):
                        files.append(f)
                        # Nested archive support
                        if is_archive(f) and _depth < _max_depth:
                            data = z.read(f)
                            files.extend(
                                [f"{f}::{inner}" for inner in list_archive_files(io.BytesIO(data), _depth+1, _max_depth)]
                            )
        elif archive_path.endswith((".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tar.xz")):
            with tarfile.open(archive_path) as t:
                for m in t.getmembers():
                    if m.isfile():
                        files.append(m.name)
                        # Nested archive support
                        if is_archive(m.name) and _depth < _max_depth:
                            f = t.extractfile(m)
                            if f:
                                data = f.read()
                                files.extend(
                                    [f"{m.name}::{inner}" for inner in list_archive_files(io.BytesIO(data), _depth+1, _max_depth)]
                                )
        elif archive_path.endswith(".gz"):
            with gzip.open(archive_path, "rb") as f:
                # GZ usually contains a single file, decompress and check if it's an archive
                data = f.read()
                if is_archive(archive_path[:-3]):
                    files.extend(list_archive_files(io.BytesIO(data), _depth+1, _max_depth))
        elif archive_path.endswith(".bz2"):
            with bz2.open(archive_path, "rb") as f:
                data = f.read()
                if is_archive(archive_path[:-4]):
                    files.extend(list_archive_files(io.BytesIO(data), _depth+1, _max_depth))
        elif archive_path.endswith(".xz") or archive_path.endswith(".lzma"):
            with lzma.open(archive_path, "rb") as f:
                data = f.read()
                if is_archive(archive_path[:-3]):
                    files.extend(list_archive_files(io.BytesIO(data), _depth+1, _max_depth))
        elif archive_path.endswith(".7z"):
            with py7zr.SevenZipFile(archive_path, mode='r') as z:
                for name in z.getnames():
                    files.append(name)
                    # Nested archive support
                    if is_archive(name) and _depth < _max_depth:
                        data = z.read([name])[name].read()
                        files.extend(
                            [f"{name}::{inner}" for inner in list_archive_files(io.BytesIO(data), _depth+1, _max_depth)]
                        )
        elif archive_path.endswith(".rar"):
            with rarfile.RarFile(archive_path) as r:
                for info in r.infolist():
                    files.append(info.filename)
                    if is_archive(info.filename) and _depth < _max_depth:
                        data = r.read(info)
                        files.extend(
                            [f"{info.filename}::{inner}" for inner in list_archive_files(io.BytesIO(data), _depth+1, _max_depth)]
                        )
        elif isinstance(archive_path, io.BytesIO):
            # Try as zip, tar, 7z, etc.
            try:
                with zipfile.ZipFile(archive_path) as z:
                    for f in z.namelist():
                        if not f.endswith("/"):
                            files.append(f)
            except Exception:
                try:
                    archive_path.seek(0)
                    with tarfile.open(fileobj=archive_path) as t:
                        for m in t.getmembers():
                            if m.isfile():
                                files.append(m.name)
                except Exception:
                    pass
        # Add more formats as needed
    except Exception:
        pass
    return files

def extract_file_from_archive(archive_path, file_inside):
    """
    Returns the contents of a file inside the archive as a string.
    Supports nested archives using '::' as a separator.
    """
    if "::" in file_inside:
        first, rest = file_inside.split("::", 1)
        data = extract_file_from_archive(archive_path, first)
        return extract_file_from_archive(io.BytesIO(data.encode("utf-8")), rest)
    archive_path = str(archive_path)
    try:
        if archive_path.endswith((".zip", ".whl", ".egg", ".jar", ".nupkg")):
            with zipfile.ZipFile(archive_path) as z:
                return z.read(file_inside).decode("utf-8", errors="ignore")
        elif archive_path.endswith((".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tar.xz")):
            with tarfile.open(archive_path) as t:
                f = t.extractfile(file_inside)
                return f.read().decode("utf-8", errors="ignore") if f else ""
        elif archive_path.endswith(".gz"):
            with gzip.open(archive_path, "rb") as f:
                return f.read().decode("utf-8", errors="ignore")
        elif archive_path.endswith(".bz2"):
            with bz2.open(archive_path, "rb") as f:
                return f.read().decode("utf-8", errors="ignore")
        elif archive_path.endswith(".xz") or archive_path.endswith(".lzma"):
            with lzma.open(archive_path, "rb") as f:
                return f.read().decode("utf-8", errors="ignore")
        elif archive_path.endswith(".7z"):
            with py7zr.SevenZipFile(archive_path, mode='r') as z:
                return z.read([file_inside])[file_inside].read().decode("utf-8", errors="ignore")
        elif archive_path.endswith(".rar"):
            with rarfile.RarFile(archive_path) as r:
                return r.read(file_inside).decode("utf-8", errors="ignore")
        elif isinstance(archive_path, io.BytesIO):
            # Try as zip, tar, 7z, etc.
            try:
                with zipfile.ZipFile(archive_path) as z:
                    return z.read(file_inside).decode("utf-8", errors="ignore")
            except Exception:
                try:
                    archive_path.seek(0)
                    with tarfile.open(fileobj=archive_path) as t:
                        f = t.extractfile(file_inside)
                        return f.read().decode("utf-8", errors="ignore") if f else ""
                except Exception:
                    pass
        # Add more formats as needed
    except Exception:
        pass
    return ""
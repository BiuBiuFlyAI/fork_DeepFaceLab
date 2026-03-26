import os
import pathlib
import typing
import shutil

from typing import List


def get_files(
        folder: pathlib.Path,
        recursion: bool = True,
        ext: typing.Optional[typing.List[str]] = None
) -> typing.List[pathlib.Path]:
    matched_files: List[pathlib.Path] = []

    if ext is not None:
        ext = [e.lower() if e.startswith('.') else f'.{e.lower()}' for e in ext]

    if recursion:
        for root, _, filenames in os.walk(folder):
            for name in filenames:
                file = pathlib.Path(root) / name
                if file.is_file() and (ext is None or file.suffix.lower() in ext):
                    matched_files.append(file.absolute().resolve())
    else:
        for name in os.listdir(folder):
            file = folder / name
            if file.is_file() and (ext is None or file.suffix.lower() in ext):
                matched_files.append(file.absolute().resolve())

    return matched_files


def move_file(
        src_path: pathlib.Path,
        dst_path_dir: pathlib.Path
):
    try:
        dst_path_dir.parent.mkdir(parents=True, exist_ok=True)
    except:
        pass

    try:
        shutil.move(str(src_path), str(dst_path_dir))
    except FileNotFoundError:
        print(f"File not found: {src_path}")
    except PermissionError:
        print(f"Permission denied: {src_path}")
    except Exception as e:
        print(f"Error moving file {src_path} -> {dst_path_dir}: {e}")


def copy_file(
        src_path: pathlib.Path,
        dst_path_or_dir: pathlib.Path
):
    try:
        dst_path_or_dir.parent.mkdir(parents=True, exist_ok=True)
    except:
        pass

    try:
        shutil.copy(src_path, dst_path_or_dir)
    except FileNotFoundError:
        print(f"File not found: {src_path}")
    except PermissionError:
        print(f"Permission denied: {src_path}")
    except Exception as e:
        print(f"Error moving file {src_path} -> {dst_path_or_dir}: {e}")

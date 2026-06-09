import sys
import math
import argparse
import pathlib
import multiprocessing
import functools
import typing

import tqdm
import psutil

import extra.base.file
import extra.base.interactive_tools

import DFLIMG


###############################################################################


def process(
        source_dir: pathlib.Path,
        dst_dir: pathlib.Path,
        aligned_path: pathlib.Path,
) -> int:
    aligned_path = aligned_path.absolute().resolve()

    dfl_img = DFLIMG.DFLJPG.load(str(aligned_path))
    if dfl_img is None:
        return 0

    source_filename = dfl_img.get_source_filename()
    if source_filename is None:
        return 0

    try:
        source_path = source_dir / source_filename
        dst_path = dst_dir / source_filename
        extra.base.file.copy_file(source_path, dst_path)
        return 1
    except:
        return 0


def do(
        aligned_dir: pathlib.Path,
        source_dir: pathlib.Path,
        dst_dir: pathlib.Path,
        num_workers: int,
) -> typing.Generator[int, None, None]:
    aligned_dir.mkdir(parents=True, exist_ok=True)
    source_dir.mkdir(parents=True, exist_ok=True)
    dst_dir.mkdir(parents=True, exist_ok=True)

    aligneds = extra.base.file.get_files(aligned_dir, recursion=False, ext=[".jpg"])

    if num_workers <= 0:
        num_workers = max(1, psutil.cpu_count() - 1)

    count = 0
    total = len(aligneds)
    yield total

    partial_process = functools.partial(process, source_dir, dst_dir)

    with multiprocessing.Pool(num_workers) as pool:
        for _ in pool.imap_unordered(func=partial_process, iterable=aligneds, chunksize=num_workers):
            count += 1
            yield count


################################################################################


def wrapper(args: argparse.Namespace):
    aligned_dir: pathlib.Path = args.aligned_dir
    source_dir: pathlib.Path = args.source_dir
    dst_dir: pathlib.Path = args.dst_dir
    num_workers: bool = args.num_workers
    std_progress: bool = args.std_progress

    running = do(
        aligned_dir=aligned_dir,
        source_dir=source_dir,
        dst_dir=dst_dir,
        num_workers=num_workers,
    )

    total = next(running)

    if std_progress:
        for count in running:
            print(
                math.floor(count / total * 100)
            )
    else:
        with tqdm.tqdm(total=total, ascii=True, ncols=80, leave=True) as bar:
            for count in running:
                bar.update(1)
        print("Finish...")


def interactive_mode() -> argparse.Namespace:
    print("复制全部面部Aligned对应的源图像")
    aligned_dir = extra.base.interactive_tools.input_path("Aligned图像目录路径")
    source_dir = extra.base.interactive_tools.input_path("源图像目录路径")
    dst_dir = extra.base.interactive_tools.input_path("输出图像目录路径")
    num_workers = extra.base.interactive_tools.input_int("并行进程数", default=0)

    return argparse.Namespace(
        aligned_dir=aligned_dir,
        source_dir=source_dir,
        dst_dir=dst_dir,
        num_workers=num_workers,
        std_progress=False,
    )


def cli_mode() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="复制全部面部Aligned对应的源图像")
    parser.add_argument("--aligned_dir", type=pathlib.Path, required=True, help="Aligned图像目录路径")
    parser.add_argument("--source_dir", type=pathlib.Path, required=True, help="源图像目录路径")
    parser.add_argument("--dst_dir", type=pathlib.Path, required=True, help="输出图像目录路径")
    parser.add_argument("--num_workers", type=int, default=0, required=False, help="并行进程数")
    parser.add_argument("--std_progress", action="store_true", help="")
    args = parser.parse_args()

    return args


################################################################################


def main():
    if "--interactive" in sys.argv:
        args = interactive_mode()
    else:
        args = cli_mode()

    wrapper(args)


if __name__ == '__main__':
    main()

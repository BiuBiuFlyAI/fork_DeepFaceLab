import sys
import math
import argparse
import pathlib
import multiprocessing
import typing
import functools

import tqdm
import numpy
import psutil
import PIL.Image
import scipy.ndimage

import extra.base.file
import extra.base.interactive_tools

import DFLIMG


###############################################################################


def process(
        aligned_dir: pathlib.Path,
        dst_dir: pathlib.Path,
        aligned_canvas_path: pathlib.Path,
):
    aligned_files = extra.base.file.get_files(aligned_dir, recursion=False, ext=[".jpg"])

    for aligned in aligned_files:
        if aligned.name == aligned_canvas_path.name:
            dst_path = dst_dir / aligned.name
            extra.base.file.copy_file(aligned, dst_path)

    return 1


def do(
        aligned_dir: pathlib.Path,
        aligned_canvas_dir: pathlib.Path,
        dst_dir: pathlib.Path,
        num_workers: int,
) -> typing.Generator[int, None, None]:
    aligned_dir.mkdir(parents=True, exist_ok=True)
    aligned_canvas_dir.mkdir(parents=True, exist_ok=True)
    dst_dir.mkdir(parents=True, exist_ok=True)

    aligned_canvas_files = extra.base.file.get_files(aligned_canvas_dir, recursion=False, ext=[".jpg"])

    if num_workers <= 0:
        num_workers = max(1, psutil.cpu_count() - 1)

    count = 0
    total = len(aligned_canvas_files)
    yield total

    partial_process = functools.partial(process, aligned_dir, dst_dir)

    with multiprocessing.Pool(num_workers) as pool:
        for _ in pool.imap_unordered(func=partial_process, iterable=aligned_canvas_files, chunksize=num_workers):
            count += 1
            yield count


################################################################################


def wrapper(args: argparse.Namespace):
    aligned_dir: pathlib.Path = args.aligned_dir
    aligned_canvas_dir: pathlib.Path = args.aligned_canvas_dir
    dst_dir: pathlib.Path = args.dst_dir
    num_workers: bool = args.num_workers
    std_progress: bool = args.std_progress

    running = do(
        aligned_dir=aligned_dir,
        aligned_canvas_dir=aligned_canvas_dir,
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
    print("复制全部面部画布对应的Aligned图像")
    aligned_dir = extra.base.interactive_tools.input_path("Aligned目录路径")
    aligned_canvas_dir = extra.base.interactive_tools.input_path("面部画布目录路径")
    dst_dir = extra.base.interactive_tools.input_path("输出目录路径")
    num_workers = extra.base.interactive_tools.input_int("并行进程数", default=0)

    return argparse.Namespace(
        aligned_dir=aligned_dir,
        aligned_canvas_dir=aligned_canvas_dir,
        dst_dir=dst_dir,
        num_workers=num_workers,
        std_progress=False,
    )


def cli_mode() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="复制全部面部画布对应的Aligned图像")
    parser.add_argument("--aligned_dir", type=pathlib.Path, required=True, help="源图像目录路径")
    parser.add_argument("--aligned_canvas_dir", type=pathlib.Path, required=True, help="临时目录路径")
    parser.add_argument("--dst_dir", type=pathlib.Path, required=True, help="回收目录路径")
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

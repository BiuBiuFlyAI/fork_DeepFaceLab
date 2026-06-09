import sys
import math
import argparse
import pathlib
import multiprocessing
import typing
import functools

import tqdm
import psutil

import extra.base.file
import extra.base.interactive_tools
import extra.base.std_log
import extra.base.dfl_pickle

import DFLIMG


###############################################################################


def check_is_dfl_image(
        image_path: pathlib.Path
):
    try:
        dfl_image = DFLIMG.DFLJPG.load(str(image_path))
        if dfl_image is None:
            return False
        else:
            return True
    except Exception as e:
        return False


def process(
        image_path: pathlib.Path,
        dst_dir: pathlib.Path,
):
    with extra.base.std_log.suppress_output():
        dst_path = dst_dir / image_path.name
        check_is_dfl = check_is_dfl_image(image_path)

        if check_is_dfl:
            extra.base.file.copy_file(image_path, dst_path)
        else:
            try:
                dfl_image = DFLIMG.DFLJPG.load(str(image_path))
                dfl_image.filename = str(dst_path)
                dfl_image.save()
            except Exception as e:
                pass


def do(
        src_dir: pathlib.Path,
        dst_dir: pathlib.Path,
        num_workers: int,
) -> typing.Generator[int, None, None]:
    src_dir.mkdir(parents=True, exist_ok=True)
    dst_dir.mkdir(parents=True, exist_ok=True)

    images = extra.base.file.get_files(src_dir, recursion=True, ext=[".jpg", ".jpeg"])

    if num_workers <= 0:
        num_workers = max(1, psutil.cpu_count() - 1)

    count = 0
    total = len(images)
    yield total

    process_partial = functools.partial(process, dst_dir=dst_dir)

    with multiprocessing.Pool(num_workers) as pool:
        for _ in pool.imap_unordered(func=process_partial, iterable=images, chunksize=num_workers):
            count += 1
            yield count


################################################################################


def wrapper(args: argparse.Namespace):
    src_dir: pathlib.Path = args.src_dir
    dst_dir: pathlib.Path = args.dst_dir
    num_workers: bool = args.num_workers
    std_progress: bool = args.std_progress

    running = do(
        src_dir=src_dir,
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
    print("转换图像到DFL图像")
    src_dir = extra.base.interactive_tools.input_path("源图像目录路径")
    dst_dir = extra.base.interactive_tools.input_path("输出目录路径")
    num_workers = extra.base.interactive_tools.input_int("并行进程数", default=0)

    return argparse.Namespace(
        src_dir=src_dir,
        dst_dir=dst_dir,
        num_workers=num_workers,
        std_progress=False,
    )


def cli_mode() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="转换图像到DFL图像")
    parser.add_argument("--src_dir", type=pathlib.Path, required=True, help="源图像目录路径")
    parser.add_argument("--dst_dir", type=pathlib.Path, required=True, help="输出目录路径")
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

import sys
import math
import argparse
import pathlib
import multiprocessing
import typing
import functools
import os

import tqdm
import numpy
import psutil
import PIL.Image

import extra.base.file
import extra.base.interactive_tools
import extra.base.std_log
import extra.base.dfl_pickle

import DFLIMG


###############################################################################


def process(
        image_path: pathlib.Path,
        mask_dir: pathlib.Path,
        dst_dir: pathlib.Path,
):
    mask_path = mask_dir / image_path.name
    dst_path = dst_dir / image_path.name

    if not mask_path.exists() or not image_path.is_file():
        return

    with extra.base.std_log.suppress_output():
        try:
            image = DFLIMG.DFLJPG.load(str(image_path))
        except Exception as e:
            return

        if image is None:
            return

    mask = PIL.Image.open(mask_path)
    mask = mask.convert("L")
    mask = mask.resize(
        size=(256, 256),
        resample=PIL.Image.Resampling.BICUBIC,
    )
    mask = numpy.asarray(mask, dtype=numpy.float32)
    mask = mask / 255.0

    image.set_xseg_mask(mask)

    try:
        image.filename = str(dst_path)
        image.save()
    except Exception as e:
        os.remove(dst_path)


def do(
        image_dir: pathlib.Path,
        mask_dir: pathlib.Path,
        dst_dir: pathlib.Path,
        num_workers: int,
) -> typing.Generator[int, None, None]:
    image_dir.mkdir(parents=True, exist_ok=True)
    mask_dir.mkdir(parents=True, exist_ok=True)
    dst_dir.mkdir(parents=True, exist_ok=True)

    images = extra.base.file.get_files(image_dir, recursion=True, ext=[".jpg", ".jpeg"])

    if num_workers <= 0:
        num_workers = max(1, psutil.cpu_count() - 1)

    count = 0
    total = len(images)
    yield total

    process_partial = functools.partial(process, mask_dir=mask_dir, dst_dir=dst_dir)

    with multiprocessing.Pool(num_workers) as pool:
        for _ in pool.imap_unordered(func=process_partial, iterable=images, chunksize=num_workers):
            count += 1
            yield count


################################################################################


def wrapper(args: argparse.Namespace):
    image_dir: pathlib.Path = args.image_dir
    mask_dir: pathlib.Path = args.mask_dir
    dst_dir: pathlib.Path = args.dst_dir
    num_workers: bool = args.num_workers
    std_progress: bool = args.std_progress

    running = do(
        image_dir=image_dir,
        mask_dir=mask_dir,
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
    print("添加面部掩码到DFL图像")
    image_dir = extra.base.interactive_tools.input_path("DFL图像目录路径")
    mask_dir = extra.base.interactive_tools.input_path("掩码目录路径")
    dst_dir = extra.base.interactive_tools.input_path("输出目录路径")
    num_workers = extra.base.interactive_tools.input_int("并行进程数", default=0)

    return argparse.Namespace(
        image_dir=image_dir,
        mask_dir=mask_dir,
        dst_dir=dst_dir,
        num_workers=num_workers,
        std_progress=False,
    )


def cli_mode() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="添加面部掩码到DFL图像")
    parser.add_argument("--image_dir", type=pathlib.Path, required=True, help="DFL图像目录路径")
    parser.add_argument("--mask_dir", type=pathlib.Path, required=True, help="掩码目录路径")
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

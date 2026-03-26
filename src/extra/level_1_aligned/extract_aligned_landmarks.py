import sys
import math
import argparse
import pathlib
import multiprocessing
import typing
import json

import tqdm
import numpy
import psutil

import extra.base.file
import extra.base.interactive_tools

import DFLIMG


################################################################################


def process(
        image: pathlib.Path
) -> dict:
    image_path = image.absolute().resolve()
    dfl_img = DFLIMG.DFLJPG.load(str(image_path))

    landmarks = dfl_img.get_landmarks()
    landmarks = numpy.round(landmarks).astype(numpy.uint32)
    landmarks = landmarks.tolist()

    return {
        "file": image.name,
        "landmarks": landmarks,
    }


def do(
        src_dir: pathlib.Path,
        dst_file: pathlib.Path,
        num_workers: int,
) -> typing.Generator[float, None, None]:
    src_dir.mkdir(parents=True, exist_ok=True)

    images = extra.base.file.get_files(src_dir, recursion=False, ext=[".jpg"])

    if num_workers <= 0:
        num_workers = max(1, psutil.cpu_count() - 1)

    count = 0
    total = len(images)
    yield total + 1

    landmarks_list = []

    with multiprocessing.Pool(num_workers) as pool:
        for landmarks in pool.imap_unordered(func=process, iterable=images, chunksize=num_workers):
            landmarks_list.append(landmarks)
            count += 1
            yield count

    with open(dst_file, "w", encoding="utf-8") as f:
        json_string = json.dumps(obj=landmarks_list, indent=4, ensure_ascii=False)
        f.write(json_string)
        f.flush()

    yield count + 1


################################################################################


def wrapper(args: argparse.Namespace):
    src_dir: pathlib.Path = args.src_dir
    dst_file: pathlib.Path = args.dst_file
    num_workers: bool = args.num_workers
    std_progress: bool = args.std_progress

    running = do(
        src_dir=src_dir,
        dst_file=dst_file,
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
    print("从DFL图像提取面部关键点")
    src_dir = extra.base.interactive_tools.input_path("源图像目录路径")
    dst_file = extra.base.interactive_tools.input_path("输出数据文件路径")
    num_workers = extra.base.interactive_tools.input_int("并行进程数", default=0)

    return argparse.Namespace(
        src_dir=src_dir,
        dst_file=dst_file,
        num_workers=num_workers,
        std_progress=False,
    )


def cli_mode() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从DFL图像提取面部关键点")
    parser.add_argument("--src_dir", type=pathlib.Path, required=True, help="源图像目录路径")
    parser.add_argument("--dst_file", type=pathlib.Path, required=True, help="输出数据文件路径")
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

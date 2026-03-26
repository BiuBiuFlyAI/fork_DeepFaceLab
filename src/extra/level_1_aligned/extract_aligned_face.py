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


def build_masked_face(
        image: numpy.ndarray,
        mask: numpy.ndarray,
        gaussian: float,
) -> PIL.Image.Image:
    mask = mask.astype(numpy.float32)
    mask = numpy.squeeze(mask, axis=-1)
    mask = PIL.Image.fromarray(mask).resize(
        size=image.shape[:2],
        resample=PIL.Image.Resampling.BICUBIC,
    )
    mask = numpy.array(mask)

    if gaussian > 0:
        mask = scipy.ndimage.gaussian_filter(mask, sigma=gaussian)  # type: ignore
        mask = numpy.clip(mask, 0, 1)

    image = image.astype(numpy.float32)
    image = image[..., [2, 1, 0]]

    masked_face_image = image * mask[..., numpy.newaxis]
    masked_face_image = masked_face_image.astype(numpy.uint8)
    masked_face_image = PIL.Image.fromarray(masked_face_image)

    return masked_face_image


def process(
        dst_dir: pathlib.Path,
        gaussian: float,
        image: pathlib.Path
) -> int:
    try:
        dfl_image_path = image.absolute().resolve()
        dfl_img = DFLIMG.DFLJPG.load(str(dfl_image_path))
    except Exception as e:
        return 0

    if dfl_img is None:
        return 0

    try:
        image = dfl_img.get_img()
        mask = dfl_img.get_xseg_mask()
    except Exception as e:
        return 0

    if image is None or mask is None:
        return 0

    masked_face_image = build_masked_face(image, mask, gaussian)
    save_path = dst_dir / f"{dfl_image_path.stem}.jpg"

    try:
        masked_face_image.save(save_path)
        masked_face_image.close()
        return 1
    except:
        return 0


def do(
        src_dir: pathlib.Path,
        dst_dir: pathlib.Path,
        gaussian: float,
        num_workers: int,
) -> typing.Generator[int, None, None]:
    src_dir.mkdir(parents=True, exist_ok=True)
    dst_dir.mkdir(parents=True, exist_ok=True)

    images = extra.base.file.get_files(src_dir, recursion=False, ext=[".jpg"])

    if num_workers <= 0:
        num_workers = max(1, psutil.cpu_count() - 1)

    count = 0
    total = len(images)
    yield total

    partial_process = functools.partial(process, dst_dir, gaussian)

    with multiprocessing.Pool(num_workers) as pool:
        for _ in pool.imap_unordered(func=partial_process, iterable=images, chunksize=num_workers):
            count += 1
            yield count


################################################################################


def wrapper(args: argparse.Namespace):
    src_dir: pathlib.Path = args.src_dir
    dst_dir: pathlib.Path = args.dst_dir
    gaussian: float = args.gaussian
    num_workers: bool = args.num_workers
    std_progress: bool = args.std_progress

    running = do(
        src_dir=src_dir,
        dst_dir=dst_dir,
        gaussian=gaussian,
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
    print("从DFL图像提取面部")
    src_dir = extra.base.interactive_tools.input_path("源图像目录路径")
    dst_dir = extra.base.interactive_tools.input_path("输出目录路径")
    gaussian = extra.base.interactive_tools.input_float("高斯模糊系数", default=0.1)
    num_workers = extra.base.interactive_tools.input_int("并行进程数", default=0)

    return argparse.Namespace(
        src_dir=src_dir,
        dst_dir=dst_dir,
        gaussian=gaussian,
        num_workers=num_workers,
        std_progress=False,
    )


def cli_mode() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从DFL图像提取面部")
    parser.add_argument("--src_dir", type=pathlib.Path, required=True, help="源图像目录路径")
    parser.add_argument("--dst_dir", type=pathlib.Path, required=True, help="输出目录路径")
    parser.add_argument("--gaussian", type=float, default=0.1, required=False, help="高斯模糊系数")
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

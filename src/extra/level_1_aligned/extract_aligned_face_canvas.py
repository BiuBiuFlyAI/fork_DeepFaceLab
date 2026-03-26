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
import PIL.ImageDraw
import scipy.ndimage
from typing import List

import extra.base.file
import extra.base.interactive_tools

import DFLIMG


###############################################################################


def get_landmarks(
        dfl_img: DFLIMG.DFLJPG,
) -> numpy.array:
    landmarks = dfl_img.get_landmarks()

    landmarks = numpy.round(landmarks).astype(numpy.int32)

    return landmarks


def get_mask(
        dfl_img: DFLIMG.DFLJPG,
) -> numpy.array:
    xseg_mask = dfl_img.get_xseg_mask()

    xseg_mask = numpy.squeeze(xseg_mask, axis=-1)  # (256, 256, 1) -> (256, 256)

    xseg_mask = xseg_mask.astype(numpy.float32)

    xseg_mask = xseg_mask * 255.0

    xseg_mask = numpy.clip(xseg_mask, 0.0, 255.0)

    xseg_mask = xseg_mask.astype(numpy.uint8)

    xseg_mask_image = PIL.Image.fromarray(xseg_mask).convert("L")

    target_size = dfl_img.get_img().shape[:2]
    xseg_mask_image = xseg_mask_image.resize(size=target_size, resample=PIL.Image.Resampling.BICUBIC)

    xseg_mask = numpy.array(xseg_mask_image).astype(numpy.float32)

    return xseg_mask


def get_image(
        dfl_img: DFLIMG.DFLJPG,
) -> numpy.array:
    image = dfl_img.get_img()

    image = image.astype(numpy.float32)

    image = image[..., [2, 1, 0]]  # BGR -> RGB

    return image


def build_face_canvas(
        image: numpy.ndarray,
        mask: numpy.ndarray,
        landmarks: numpy.ndarray,
) -> PIL.Image.Image:
    h, w, c = image.shape

    overlay_color = (0, 255, 0)  # 掩码覆盖颜色
    overlay_opacity = 0.5  # 掩码不透明度

    point_color = (255, 0, 0)  # 点颜色
    point_radius = 4  # 点半径

    image_uint8 = numpy.clip(image, 0, 255).astype(numpy.uint8)

    alpha = mask * overlay_opacity
    alpha = numpy.clip(alpha, 0, 255).astype(numpy.uint8)

    base = PIL.Image.fromarray(image_uint8).convert("RGBA")

    # 覆盖掩码
    color_img = PIL.Image.new(
        mode="RGBA",
        size=(w, h),
        color=(overlay_color[0], overlay_color[1], overlay_color[2], 0)
    )
    color_img.putalpha(PIL.Image.fromarray(alpha, mode="L"))
    composed = PIL.Image.alpha_composite(base, color_img)

    # 绘制关键点
    draw = PIL.ImageDraw.Draw(composed)
    lm = numpy.asarray(landmarks)
    for (x, y) in lm.astype(int):
        r = max(1, int(point_radius))
        bbox = (x - r, y - r, x + r, y + r)
        draw.ellipse(bbox, fill=tuple(point_color))

    return composed.convert("RGB")


def process(
        dst_dir: pathlib.Path,
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
        image = get_image(dfl_img)
        mask = get_mask(dfl_img)
        landmarks = get_landmarks(dfl_img)
    except Exception as e:
        return 0

    face_canvas = build_face_canvas(image, mask, landmarks)

    save_path = dst_dir / f"{dfl_image_path.stem}.jpg"

    try:
        face_canvas.save(save_path)
        face_canvas.close()
        return 1
    except:
        return 0


def do(
        src_dir: pathlib.Path,
        dst_dir: pathlib.Path,
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

    partial_process = functools.partial(process, dst_dir)

    with multiprocessing.Pool(num_workers) as pool:
        for _ in pool.imap_unordered(func=partial_process, iterable=images, chunksize=num_workers):
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
    print("从DFL图像提取面部画布")
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
    parser = argparse.ArgumentParser(description="从DFL图像提取面部画布")
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

import typing
import argparse
import math
import pathlib
import sys

import tqdm

import extra.base.dfl_pickle as utils_dfl_pickle
import extra.base.interactive_tools as utils_interactive_tools

################################################################################


need_key = [
    'iter',
    'options',
    'loss_history',
    'sample_for_preview',
    'choosed_gpu_indexes',
]

need_options_key = [
    'resolution', 'face_type', 'models_opt_on_gpu',
    'archi', 'ae_dims', 'e_dims', 'd_dims', 'd_mask_dims',
    'masked_training', 'uniform_yaw', 'lr_dropout',
    'random_warp', 'gan_power', 'true_face_power',
    'face_style_power', 'bg_style_power', 'ct_mode',
    'clipgrad', 'pretrain', 'autobackup_hour',
    'write_preview_history', 'target_iter', 'random_flip',
    'batch_size', 'eyes_mouth_prio', 'adabelief',
    'gan_patch_size', 'gan_dims',
    'random_src_flip', 'random_dst_flip'
]

need_default_options_key = [
    'resolution', 'face_type', 'models_opt_on_gpu',
    'archi', 'ae_dims', 'e_dims', 'd_dims', 'd_mask_dims',
    'masked_training', 'eyes_prio', 'uniform_yaw', 'lr_dropout',
    'random_warp', 'gan_power', 'true_face_power',
    'face_style_power', 'bg_style_power', 'ct_mode',
    'clipgrad', 'pretrain', 'autobackup_hour',
    'write_preview_history',
    'target_iter', 'random_flip', 'batch_size',
]


################################################################################


def _del_keys(
        data: dict,
        all_key: typing.List[str],
        need_key: typing.List[str]
):
    need_del_key = [k for k in all_key if k not in need_key]

    for k in need_del_key:
        del data[k]


def _get_model_file_name(model_name: str) -> str:
    model_data_name = f"{model_name}_SAEHD_data.dat"

    return model_data_name


################################################################################


def clean_model_data(data: dict):
    all_key = list(data.keys())
    all_options_key = list(data["options"].keys())

    _del_keys(data, all_key, need_key)
    _del_keys(data["options"], all_options_key, need_options_key)


def clean_model_default_options(data: dict):
    all_key = list(data.keys())

    _del_keys(data, all_key, need_default_options_key)


def clean_model_train_log(data: dict):
    data["iter"] = 1
    data["loss_history"] = [[0.0, 0.0]]

    try:
        del data["sample_for_preview"]
    except KeyError:
        pass


###############################################################################


def do(
        model_dir: pathlib.Path,
        model_name: str,
        clean_train_log: bool,
) -> typing.Generator[int, None, None]:
    model_data_name = _get_model_file_name(model_name)

    model_data_path = model_dir / model_data_name
    model_data = utils_dfl_pickle.pickle_load(model_data_path)
    clean_model_data(model_data)

    if clean_train_log:
        clean_model_train_log(model_data)

    utils_dfl_pickle.pickle_write(model_data_path, model_data)

    count = 1
    total = 1

    yield total
    yield count


################################################################################


def wrapper(args: argparse.Namespace):
    model_dir: pathlib.Path = args.model_dir
    model_name: str = args.model_name
    clean_train_log: bool = args.clean_train_log
    std_progress: bool = args.std_progress

    running = do(
        model_dir=model_dir,
        model_name=model_name,
        clean_train_log=clean_train_log,
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
    print("清理SAHED模型元数据")
    model_dir = utils_interactive_tools.input_path("模型目录路径")
    model_name = utils_interactive_tools.input_str("模型名称", default="new")
    clean_train_log = utils_interactive_tools.input_bool("清理训练数据")

    return argparse.Namespace(
        model_dir=model_dir,
        model_name=model_name,
        clean_train_log=clean_train_log,
        std_progress=False,
    )


def cli_mode() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="清理SAHED模型元数据")
    parser.add_argument("--model_dir", type=pathlib.Path, required=True, help="模型目录路径")
    parser.add_argument("--model_name", type=str, default="new", required=True, help="模型名称")
    parser.add_argument("--clean_train_log", action="store_true", help="清理训练数据")
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

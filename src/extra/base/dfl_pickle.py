import pathlib
import pickle


def pickle_load(data_path: pathlib.Path) -> dict:
    with open(data_path, 'rb') as f:
        data = pickle.load(file=f)
        return data


def pickle_write(data_path: pathlib.Path, data: dict):
    with open(data_path, 'wb') as f:
        # >= python 3.4
        pickle.dump(obj=data, file=f, protocol=4)  # type: ignore

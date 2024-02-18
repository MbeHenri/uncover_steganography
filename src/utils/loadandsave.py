import json
from pickle import dump, load


def load2json(path_ext_img):
    with open(path_ext_img, "r") as f:
        extensions_images = json.load(f)
    return extensions_images


def save_model(result, file_path):
    with open(file_path, "wb") as f:
        dump(result, f)


def load_model(file_path):
    with open(file_path, "rb") as f:
        model = load(f)
    return model


def save2json(obj, path_file):
    with open(path_file, "w") as fichier_json:
        json.dump(obj, fichier_json)


def load_txt(path_file):
    with open(path_file, "r") as f:
        msg = f.read()
    return msg


def save_txt(path_file, texte):
    with open(path_file, "w") as f:
        f.write(texte)

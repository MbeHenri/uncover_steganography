import os
from PIL import Image
from src.utils.functions import preprocessing
from src.utils.loadandsave import load2json


def extract(
    path_sl="sl.json",
    path_slid="slid.json",
    path_imgs="./send_imgs",
    path_indexdb="./indexdb",
    path_conf="conf.json",
):
    params = load2json(os.path.join(path_indexdb, "params.json"))

    conf = load2json(path_conf)
    SL = load2json(path_sl)
    SLid = load2json(path_slid)
    image = Image.new("L", (conf["Iw"], conf["Ih"]), "white")

    i = 0

    y = 0
    while (y + params["Ph"]) <= conf["Ih"]:
        x = 0
        while (x + params["Pw"]) <= conf["Iw"]:
            id = SLid[i]
            if id is not None:
                natural_image = preprocessing(
                    os.path.join(path_imgs, f"{i}.png"), need_resize=False
                )
                position = SL[id]
                duplicate_patch = natural_image.crop(
                    (
                        position["x"],
                        position["y"],
                        position["x"] + params["Pw"],
                        position["y"] + params["Ph"],
                    )
                )
                image.paste(duplicate_patch, (x, y))
            i += 1
            x += params["Pw"]
        y += params["Ph"]

    return image

import os
from PIL import Image
from src.utils.functions import preprocessing
from src.utils.loadandsave import load2json


def extracting(
    path_sl="sl.json",
    path_slid="slid.json",
    path_imgs="./send_imgs",
    path_indexdb="./indexdb",
    key=None,
):
    params = load2json(os.path.join(path_indexdb, "params.json"))

    SL = load2json(path_sl)
    SLid = load2json(path_slid)
    image = Image.new("L", (params["Iw"], params["Ih"]), "white")

    i = 0
    for y in range(0, image.height, params["Ph"]):
        for x in range(0, image.width, params["Pw"]):
            id = SLid[i]
            if id is not None:
                natural_image = preprocessing(
                    os.path.join(path_imgs, f"{i}.png"),
                    Iw=params["Iw"],
                    Ih=params["Ih"],
                )
                duplicate_patch = natural_image.crop(
                    (
                        SL[id]["x"],
                        SL[id]["y"],
                        SL[id]["x"] + params["Pw"],
                        SL[id]["y"] + params["Ph"],
                    )
                )
                image.paste(duplicate_patch, (x, y))
            i += 1

    return image

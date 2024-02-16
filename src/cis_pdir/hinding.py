import numpy as np
from PIL import Image
import os
from src.utils.functions import concat_list_features, cutting, extraction_features_histogram, hashing_mean, patching, preprocessing

from src.utils.loadandsave import load2json, load_model, save2json

def distance(x, y):
    x = np.array(x)
    y = np.array(y)
    return np.sum(np.sum((x - y) ** 2))


def search(f, datas: list):
    n = len(datas)
    db = None
    if n > 0:
        dmin = None
        for i in range(n):
            d = distance(datas[i]["data"], f)
            if dmin is not None:
                if dmin > d:
                    db = datas[i]
                    dmin = d
            else:
                db = datas[i]
                dmin = d
    return db
    

def hinding(
    path_secret_image,
    path_sl="sl.json",
    path_slid="slid.json",
    path_imgs="./send_imgs",
    path_indexdb="./indexdb",
    key=None,
):
    params = load2json(os.path.join(path_indexdb, "params.json"))

    image_secret = preprocessing(path_secret_image, Iw=params["Iw"], Ih=params["Ih"])

    patchs, _ = patching(image_secret, Pw=params["Pw"], Ph=params["Ph"])

    PB = len(patchs)
    indexfiles = load_model(os.path.join(path_indexdb, "indexfiles.pkl"))

    dir_imgs = os.path.join(path_indexdb, "imgs")
    
    SLid = []
    for i in range(PB):
        blocs, _ = cutting(patchs[i], n=params["n"], m=params["m"])
        hashcode = hashing_mean(blocs)
        data = concat_list_features(
            extraction_features_histogram(blocs),
        )
        duplicate_patchs = indexfiles.getDuplicatesDatas(data, hashcode)
        best_duplicate_patch = (
            None if duplicate_patchs is None else search(data, duplicate_patchs)
        )

        if best_duplicate_patch is not None:
            natural_image_ID = f"{best_duplicate_patch['IDC']}"
            image = Image.open(os.path.join(dir_imgs, f"{natural_image_ID}.png"))
            image.save(os.path.join(path_imgs, f"{i}.png"))

        SLid.append(
            None if best_duplicate_patch is None else best_duplicate_patch["ID"]
        )

    save2json(SLid, path_slid)
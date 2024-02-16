from src.utils.functions import cutting, hashing_eign, preprocessing
from src.utils.loadandsave import load2json


def extract(
    path_cover_image,
    path_sl="sl.json",
    path_conf="conf.json",
    unknow_car="_",
):
    SL = load2json(path_sl)
    conf = load2json(path_conf)
    cover_image = preprocessing(path_cover_image, Iw=conf["W"], Ih=conf["H"])

    n = len(SL)
    msg = []
    for i in range(n):
        position = SL[i]
        if position is not None:
            patch = cover_image.crop(
                (
                    position["x"],
                    position["y"],
                    position["x"] + conf["L"],
                    position["y"] + conf["L"],
                )
            )
            blocs, _ = cutting(patch, n=3, m=3)
            hashcode = int(
                hashing_eign(blocs, type_hash=conf["type_hash"]),
                2,
            )
            msg.append(chr(hashcode))
        else:
            msg.append(unknow_car)

    return "".join(msg)

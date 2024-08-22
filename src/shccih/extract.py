from src.utils.functions import cutting, hashing_eign, preprocessing
from src.utils.loadandsave import load2json
from src.utils.pallier import decrypt

def extract(
    path_cover_image,
    path_sl="sl.json",
    path_conf="conf.json",
    path_public_key="./pubk.json",
    path_private_key="./prik.json",
    path_sub_key="./psk.json",
    unknow_car="_",
):
    SaveSL = load2json(path_sl)
    conf = load2json(path_conf)
    cover_image = preprocessing(path_cover_image, Iw=conf["W"], Ih=conf["H"])

    # décryptage du fichier de localisation
    public_key = load2json(path_public_key)
    private_key = load2json(path_private_key)
    n = decrypt(public_key, private_key, SaveSL["n"])
    SL = [
        {
            "s": decrypt(public_key, private_key, position["s"]),
            "x": decrypt(public_key, private_key, position["x"]),
            "y": decrypt(public_key, private_key, position["y"]),
        }
        for position in SaveSL["SL"]
    ]

    # décodage du message
    ns = len(SL)
    msg = []
    key = load2json(path_sub_key)
    r_key = {v: int(k) for k, v in key.items()}
    for i in range(n):
        found = False
        j = 0
        while not found and j < ns:
            if SL[j]["s"] == i:
                patch = cover_image.crop(
                    (
                        SL[j]["x"],
                        SL[j]["y"],
                        SL[j]["x"] + conf["L"],
                        SL[j]["y"] + conf["L"],
                    )
                )
                blocs, _ = cutting(patch, n=3, m=3)
                hashcode = int(
                    hashing_eign(blocs, type_hash=conf["type_hash"]),
                    2,
                )
                msg.append(chr(r_key[hashcode]))
                found = True
            j += 1

        if not found:
            msg.append(unknow_car)
            
    return "".join(msg)

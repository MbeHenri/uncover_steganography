from src.utils.functions import cutting, hashing_eign, patching, preprocessing
from src.utils.loadandsave import save2json, load2json
from src.utils.pallier import encrypt


class LookupTable:
    def __init__(self, hashcodes: list, positions: list) -> None:
        self.table = []
        self.n = len(hashcodes)
        # self.hash_bound = {}
        for i in range(self.n):
            self.table.append(
                {
                    "hashcode": hashcodes[i],
                    "position": positions[i],
                    "mask": 0,
                }
            )
            # self.hash_bound[hashcodes[i]] = 1

    def match(self, car: int, randomed: bool = False):
        pos = None
        offset = None
        current_diff = None

        if not randomed:
            for i in range(self.n):
                if self.table[i]["mask"] != 1:
                    diff = (car - self.table[i]["hashcode"]) ** 2

                    if diff == 0:
                        self.table[i]["mask"] = 1
                        return self.table[i]["position"], 0
                    else:
                        if current_diff is not None:
                            if current_diff > diff:
                                current_diff = diff
                                pos = self.table[i]["position"]
                                offset = car - self.table[i]["hashcode"]
                        else:
                            current_diff = diff
                            pos = self.table[i]["position"]
                            offset = car - self.table[i]["hashcode"]

        return pos, offset


def hide(
    path_cover_image,
    secret_message: str,
    W: int = 512,
    H: int = 512,
    L: int = 9,
    type_hash="type2",
    path_sl="sl.json",
    path_offset="offset.json",
    path_conf="conf.json",
    path_public_key="./pubk.json",
):
    cover_image = preprocessing(path_cover_image, Iw=W, Ih=H)

    patchs, positions = patching(cover_image, Pw=L, Ph=L)

    PB = len(patchs)
    hashcodes = []
    for i in range(PB):
        blocs, _ = cutting(patchs[i], n=3, m=3)
        hashcode = int(hashing_eign(blocs, type_hash=type_hash), 2)
        hashcodes.append(hashcode)
    # print(set(hashcodes))
    lookupTable = LookupTable(hashcodes, positions)
    msg_ascii = [ord(caractere) for caractere in secret_message]
    
    SL = []
    OFFSETS = {}
    n = len(msg_ascii)
    ideal = True
    for i in range(n):
        #print(msg_ascii[i], chr(msg_ascii[i]))
        position, offset = lookupTable.match(msg_ascii[i])
        if position:
            SL.append(
                {
                    "s": i,
                    "x": position["x"],
                    "y": position["y"],
                }
            )
            OFFSETS[i] = offset
        else:
            ideal = False

    # cyptage et sauvegarde des informations de localisation
    public_key = load2json(path_public_key)
    SL = [
        {
            "s": encrypt(public_key, position["s"]),
            "x": encrypt(public_key, position["x"]),
            "y": encrypt(public_key, position["y"]),
        }
        for position in SL
    ]
    # cryptage des offsets
    # OFFSETS = {
    #   encrypt(public_key, k): encrypt(public_key, v) for k, v in OFFSETS.items()
    # }

    SaveSL = {"n": encrypt(public_key, n), "SL": SL}
    save2json(SaveSL, path_sl)
    save2json(OFFSETS, path_offset)
    save2json({"L": L, "W": W, "H": H, "type_hash": type_hash}, path_conf)

    # print(lookupTable.table)
    return ideal

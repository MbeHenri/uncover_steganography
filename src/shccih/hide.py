from src.utils.functions import cutting, hashing_eign, patching, preprocessing
from src.utils.loadandsave import save2json, load2json
from src.utils.pallier import encrypt
from src.utils.substitution import generate_substitution_key


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

    def match(self, car: int):
        pos = None
        try:
            i = 0
            ok = False
            while not ok and i < self.n:
                if self.table[i]["hashcode"] == car and self.table[i]["mask"] != 1:
                    pos = self.table[i]["position"]
                    self.table[i]["mask"] = 1
                    ok = True
                i += 1
        except KeyError:
            pass
        return pos


def hide(
    path_cover_image,
    secret_message: str,
    W: int = 512,
    H: int = 512,
    L: int = 9,
    type_hash="type2",
    path_sl="sl.json",
    path_conf="conf.json",
    path_public_key="./pubk.json",
    path_sub_key="./psk.json",
):
    cover_image = preprocessing(path_cover_image, Iw=W, Ih=H)

    patchs, positions = patching(cover_image, Pw=L, Ph=L)

    PB = len(patchs)
    hashcodes = []
    for i in range(PB):
        blocs, _ = cutting(patchs[i], n=3, m=3)
        hashcode = int(hashing_eign(blocs, type_hash=type_hash), 2)
        hashcodes.append(hashcode)

    lookupTable = LookupTable(hashcodes, positions)

    # masquage du message
    key = generate_substitution_key()
    save2json(key, path_sub_key)
    
    msg_ascii = [key[ord(caractere)] for caractere in secret_message]
    SL = []
    n = len(msg_ascii)
    ideal = True
    for i in range(n):
        position = lookupTable.match(msg_ascii[i])
        if position:
            SL.append(
                {
                    "s": i,
                    "x": position["x"],
                    "y": position["y"],
                }
            )
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
    SaveSL = {"n": encrypt(public_key, n), "SL": SL}
    save2json(SaveSL, path_sl)
    save2json({"L": L, "W": W, "H": H, "type_hash": type_hash}, path_conf)
    
    return ideal

from src.utils.functions import cutting, hashing_eign, patching, preprocessing
from src.utils.loadandsave import save2json


class LookupTable:
    def __init__(self, hashcodes: list, positions: list) -> None:
        self.table = []
        self.n = len(hashcodes)
        self.hash_bound = {}
        for i in range(self.n):
            self.table.append(
                {
                    "hashcode": hashcodes[i],
                    "position": positions[i],
                    "mask": 0,
                }
            )
            self.hash_bound[hashcodes[i]] = 1

    def match(self, car: int):
        pos = None
        ok = True
        try:
            while ok:
                founded = False
                for i in range(self.n):
                    founded = self.table[i]["hashcode"] == car or founded
                    if (
                        self.table[i]["hashcode"] == car
                        and self.table[i]["mask"] < self.hash_bound[car]
                    ):
                        pos = self.table[i]["position"]
                        self.table[i]["mask"] += 1

                if pos is not None:
                    ok = False
                else:
                    if founded:
                        self.hash_bound[car] += 1
                    else:
                        ok = False
        except KeyError:
            return None
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
    msg_ascii = [ord(caractere) for caractere in secret_message]

    SL = []
    n = len(msg_ascii)
    for i in range(n):
        position = lookupTable.match(msg_ascii[i])
        SL.append(position)

    save2json(SL, path_sl)
    save2json({"L": L, "W": W, "H": H, "type_hash": type_hash}, path_conf)

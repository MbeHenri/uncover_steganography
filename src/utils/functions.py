from PIL import Image
import os
import numpy as np


def preprocessing(path_image, Iw=640, Ih=480, need_resize=True):
    image = Image.open(path_image)
    if need_resize:
        image = image.resize((Iw, Ih))
    return image.convert("L")


def patching(image, Pw=64, Ph=48):
    Iw, Ih = image.size

    blocs = []
    positions = []
    # Découper l'image en blocs de taille spécifiée
    y = 0
    while (y + Ph) <= Ih:
        x = 0
        while (x + Pw) <= Iw:
            box = (x, y, x + Pw, y + Ph)
            positions.append({"x": x, "y": y})
            blocs.append(
                image.crop(box),
            )
            x += Pw
        y += Ph

    return blocs, positions


def cutting(image, n=4, m=4):
    Pw, Ph = image.size
    Bw = Pw // n
    Bh = Ph // m
    blocs = []
    positions = []

    for j in range(m):
        for i in range(n):
            x0 = i * Bw
            y0 = j * Bh
            x1 = x0 + Bw
            y1 = y0 + Bh
            positions.append({"x": x0, "y": y0})
            blocs.append(
                image.crop((x0, y0, x1, y1)),
            )

    return blocs, positions


def mean_pixels(image):
    largeur, hauteur = image.size
    pixels = image.load()

    total = 0
    nb_pixels = 0

    for y in range(hauteur):
        for x in range(largeur):
            # Récupérer la valeur du pixel
            valeur_pixel = pixels[x, y]

            # Si l'image est en couleur, calculer la moyenne des canaux RGB
            if isinstance(valeur_pixel, tuple):
                valeur_pixel = sum(valeur_pixel) / 3  # moyenne des canaux R, G, B

            total += valeur_pixel
            nb_pixels += 1

    # Calculer la moyenne des pixels
    moyenne_pixels = total / nb_pixels
    return moyenne_pixels


def extraction_features_histogram(blocs):
    # on peut voir un bloc du patch d'image comme une vue de l'image
    B = len(blocs)
    return [blocs[i].histogram() for i in range(B)]


def concat_list_features(list_features):
    result = []
    for vecteur in list_features:
        result.extend(vecteur)
    return result


def regroup_datas(datas: list, labels: list):
    result = {}
    unique_labels = []
    for i, label in enumerate(labels):
        if label not in result:
            result[label] = [datas[i]]
            unique_labels.append(label)
        else:
            result[label].append(datas[i])

    return result


def createdir(path_dir):
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)


def hashing_mean(blocs):
    B = len(blocs)
    V = [mean_pixels(blocs[i]) for i in range(B)]
    hashcode = []
    for i in range(B - 1):
        hashcode.append("1" if V[i] >= V[i + 1] else "0")
    return "".join(hashcode)


def eign_max(image):
    eigenvalues, _ = np.linalg.eig(np.array(image))
    return np.max(eigenvalues)


def hashing_eign(blocs: list, type_hash="type2"):
    B = len(blocs)
    if B == 9:
        V = [eign_max(blocs[i]) for i in range(B)]
        hashcode = []
        if type_hash == "type4":
            for i in range(9):
                if i != 4:
                    hashcode.append("1" if V[4] >= V[i + 1] else "0")
        else:
            for i in range(8):
                hashcode.append("1" if V[i] >= V[i + 1] else "0")

        return "".join(hashcode)

    return None

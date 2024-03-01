import os
from src.cis_pdir.indexdb import IndexFilesBow
from src.utils.functions import (
    concat_list_features,
    createdir,
    cutting,
    extraction_features_histogram,
    hashing_mean,
    patching,
    preprocessing,
)

from src.utils.loadandsave import load2json, save2json, save_model


def get_images(
    chemin_dossier,
    Iw: int = 640,
    Ih: int = 480,
    path_ext_img="./ext_img.json",
):
    images = []
    # Extensions d'images prises en charge
    # Charger le fichier JSON
    extensions_images = load2json(path_ext_img)

    # Parcourir les fichiers du dossier
    for nom_fichier in os.listdir(chemin_dossier):
        chemin_fichier = os.path.join(chemin_dossier, nom_fichier)

        # Vérifier si le fichier est une image en vérifiant son extension
        
        try:
            if os.path.isfile(chemin_fichier) and any(
                chemin_fichier.lower().endswith(ext) for ext in extensions_images
            ):
                images.append(
                    preprocessing(
                        chemin_fichier,
                        Ih=Ih,
                        Iw=Iw,
                        need_resize=False,
                    )
                )
        except Exception:
            pass
    return images


def construct_indexfiles(
    input_path_images="./images",
    output_path_db="./indexdb",
    path_sl="sl.json",
    Iw: int = 640,
    Ih: int = 480,
    Pw: int = 64,
    Ph: int = 48,
    n: int = 4,
    m: int = 4,
    K: int = 2,
    L: int = 3,
):
    # sauvegarde des paramètres de prétraitement et de découpage dans le dossier de sortie
    save2json(
        {"Pw": Pw, "Ph": Ph, "n": n, "m": m},
        os.path.join(output_path_db, "params.json"),
    )

    # on recupere les images avec prétraitement
    images = get_images(input_path_images)

    # patching des images en conservation les positions
    C = []
    patchs = []
    positions = []
    nb = len(images)
    for i in range(nb):
        list_patchs, list_positions = patching(images[i], Pw=Pw, Ph=Ph)
        C.extend([i for _ in list_patchs])
        patchs.extend(list_patchs)
        positions.extend(list_positions)

    ## sauvegardes
    # sauvegarde des images naturelles prétraitées dans le dossier de sortie
    dir_patch = os.path.join(output_path_db, "imgs")
    createdir(dir_patch)
    for i in range(nb):
        images[i].save(os.path.join(dir_patch, f"{i}.png"))

    # sauvegarde des positions
    save2json(positions, path_sl)

    # extraction de caractéristiques et hashage des patchs d'images
    patch_datas = []
    hashcodes = []
    PB = len(patchs)
    for i in range(PB):
        blocs, _ = cutting(patchs[i], n=n, m=m)
        patch_datas.append(
            {
                "ID": i,
                "IDC": f"{C[i]}",
                "data": concat_list_features(
                    extraction_features_histogram(blocs),
                ),
            }
        )
        hashcodes.append(hashing_mean(blocs))

    # Construction de la structure de la base de patchs d'images d'indexage inversé
    result = IndexFilesBow(K=K, L=L)
    result.construct(
        patch_datas=patch_datas,
        hashcodes=hashcodes,
    )
    save_model(result, os.path.join(output_path_db, "indexfiles.pkl"))

    return result

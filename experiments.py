from src.hccih.extract import extract as extract_hccih
from src.hccih.hide import hide as hide_hccih
from src.chccih.extract import extract as extract_chccih
from src.chccih.hide import hide as hide_chccih
from src.utils.attacks import (
    median_filter,
    gaussian_noise,
    salt_and_pepper_noise,
    speckle_noise,
)
from src.utils.metrics import BER, ER
from src.utils.loadandsave import save2json

from PIL import Image

secret_msg = "Ceci un message secret pour effectuer les expérimentations"
path_image = "./deri.jpeg"
path_image_noise = "./deri{}.jpeg"


# attaques sur image
def median3x3(image):
    return median_filter(image, 3)


def median5x5(image):
    return median_filter(image, 5)


def speckle1(image):
    return speckle_noise(image, 0.01)


def speckle5(image):
    return speckle_noise(image, 0.05)


def salt_and_pepper1(image):
    return salt_and_pepper_noise(image, 0.001, 0.001)


def salt_and_pepper5(image):
    return salt_and_pepper_noise(image, 0.005, 0.005)


def gaussian_noise1(image):
    return gaussian_noise(image, 0, 0.001)


def gaussian_noise5(image):
    return gaussian_noise(image, 0, 0.005)


attacks = {
    "median_3x3": median3x3,
    "median_5x5": median5x5,
    "gaussian_noise_0.001": gaussian_noise1,
    "gaussian_noise_0.005": gaussian_noise5,
    "salt_and_pepper_1%": salt_and_pepper1,
    "salt_and_pepper_5%": salt_and_pepper5,
    "speckle_0.01": speckle1,
    "speckle_0.05": speckle5,
}

# methode de stéganographie
methods = {
    "hccih": {
        "hide": hide_hccih,
        "extract": extract_hccih,
    },
    "chccih": {
        "hide": hide_chccih,
        "extract": extract_chccih,
    },
}

# metriques d'évaluation
metrics = {"BER": BER, "ER": ER}

# boucle d'expérimentations
perfs = {"BER": [], "ER": []}

image = Image.open(path_image)
for name_attack, attack in attacks.items():
    # attack image
    imagenoise = attack(image)
    image.save(path_image_noise.format(name_attack))

    for name_method, method in methods.items():
        # hide message
        method["hide"](path_image, secret_msg)

        # extract message
        extract_msg = method["extract"](path_image_noise.format(name_attack))

        # evaluate
        for name_metric, metric in metrics.items():
            perfs[name_metric].append(
                {
                    "method": name_method,
                    "attack": name_attack,
                    "val": metric(secret_msg, extract_msg),
                }
            )

save2json(perfs, "./perfs.json")

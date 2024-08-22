from PIL import Image, ImageFilter
import numpy as np
import random

# Attaque : Bruit de chatoiement
def speckle_noise(image, intensity):
    width, height = image.size
    pixels = image.load()
    for i in range(width):
        for j in range(height):
            r = min(255, max(0, int(pixels[i, j][0] * random.uniform(1 - intensity, 1 + intensity))))
            g = min(255, max(0, int(pixels[i, j][1] * random.uniform(1 - intensity, 1 + intensity))))
            b = min(255, max(0, int(pixels[i, j][2] * random.uniform(1 - intensity, 1 + intensity))))
            pixels[i, j] = (r, g, b)
    return image

# Attaque : Bruit de sel et de poivre
def salt_and_pepper_noise(image, salt_prob, pepper_prob):
    width, height = image.size
    pixels = image.load()
    for i in range(width):
        for j in range(height):
            if random.random() < salt_prob:
                pixels[i, j] = (255, 255, 255)  # Sel
            elif random.random() < pepper_prob:
                pixels[i, j] = (0, 0, 0)  # Poivre
    return image

# Attaque : Bruit gaussien
def gaussian_noise(image, mean, stddev):
    np_image = np.array(image)
    noise = np.random.normal(mean, stddev, np_image.shape)
    noisy_image = np.clip(np_image + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)

# Attaque : Filtre médian
def median_filter(image, size):
    return image.filter(ImageFilter.MedianFilter(size=size))
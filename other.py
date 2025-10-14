import numpy as np
from PIL import Image

# THIS FILE has nothing to do with the project <3

def c(x):
    if x <= 0.04045:
        return x / 12.92
    return ((x + 0.055) / 1.055) ** 2.4


def is_grayscale(data: np.array):
    return type(data[0][0]) == np.float64


def linearze(data: np.array):
    for i in range(data.shape[0]):
        row = data[i].copy()
        for j in range(row.shape[0]):
            pixel = row[j].copy()
            new_pixel = []
            if not is_grayscale(data):
                for v in pixel:
                    normalized = v / 255
                    new_pixel.append(c(normalized))
            else:
                normalized = pixel / 255
                new_pixel.append(c(normalized))
            data[i][j] = new_pixel
    return data


def color_channels(data: np.array):
    return data[:, :, 0], data[:, :, 1], data[:, :, 2]


def color_analysis(data: np.array):
    if is_grayscale(data):
        return 0.00, 0.00, 0.00

    red, green, blue = color_channels(data)
    return round(float(np.mean(red)), 2), \
        round(float(np.mean(green)), 2), \
        round(float(np.mean(blue)), 2)


def avg_luminance(analysis: tuple[float, float, float]):
    return round((0.2126 * analysis[0]) + (0.7152 * analysis[1]) + (0.0722 * analysis[2]), 2)


def main():
    img = Image.open("color_image.jpeg")
    data = np.array(img, dtype=np.float64)
    data = linearze(data)
    analysis = color_analysis(data)
    print(analysis)
    print(avg_luminance(analysis))


if __name__ == "__main__":
    main()

import numpy as np
from scipy.ndimage import convolve

def read_data(filename):
    with open(filename) as f:
        enhancement, image = f.read().strip().split("\n\n")

    enhancement = np.array([1 if x == "#" else 0 for x in enhancement])
    image = np.array([[1 if x == "#" else 0 for x in row.strip()] for row in image.strip().split("\n")])

    return enhancement, image

def enhancement_step(image, image_filter, enhancement, infinite_fill=0):
    # 1. grow the image 3 by 3 all around
    image = np.pad(image, 3, constant_values=infinite_fill)
    # 2. convolve the filter over the image to get a new array of enhancement lookups
    image = convolve(image, image_filter)
    # 3. new image is then the enhancement filter at teh index provided by the convolution
    enhanced_image = enhancement[image]

    return enhanced_image

# Need to consider the infinite fill. If the start of the enhancement
# is zero then it is always zero, otherwise it is 0 -> 1 -> 0 etc
def apply_enhancement(image, image_filter, enhancement, n):
    for i in range(n):
        image = enhancement_step(
            image,
            image_filter,
            enhancement,
            infinite_fill= (i%2) * enhancement[0]
        )

    return image

enhancement, image = read_data("data-day20.txt")

# for some reason this is the opposite way round from what I would expect
image_filter = np.array([
    [1,2,4],
    [8,16,32],
    [64,128,256]
])

print(apply_enhancement(image, image_filter, enhancement, n=50).sum())

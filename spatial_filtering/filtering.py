from dip import zeros
import math


class Filtering:

    def __init__(self, image):
        self.image = image

    def get_gaussian_filter(self):
        """Initialzes/Computes and returns a 5X5 Gaussian filter"""
        size = 5
        sigma = 1.0
        kernel = zeros((size, size))
        total = 0.0

        for x in range(size):
            for y in range(size):
                offset_x = x - size // 2
                offset_y = y - size // 2
                exponent = -(offset_x ** 2 + offset_y ** 2) / (2 * sigma ** 2)
                kernel[x][y] = math.exp(exponent) / (2 * math.pi * sigma ** 2)
                total += kernel[x][y]

        
        for x in range(size):
            for y in range(size):
                kernel[x][y] /= total

        return kernel

    def get_laplacian_filter(self):
        """Initialzes and returns a 3X3 Laplacian filter"""
        kernel = [
            [0, -1, 0],
            [-1, 4, -1],
            [0, -1, 0]
        ]
        return kernel

    def filter(self, filter_name):
        """Perform filtering on the image using the specified filter, and returns a filtered image
            takes as input:
            filter_name: a string, specifying the type of filter to use ["gaussian", laplacian"]
            return type: a 2d numpy array
        """
        if filter_name == "gaussian":
            kernel = self.get_gaussian_filter()
            k_size = 5
        elif filter_name == "laplacian":
            kernel = self.get_laplacian_filter()
            k_size = 3
        else:
            return self.image

        rows = len(self.image)
        cols = len(self.image[0])
        pad = k_size // 2

        
        padded_img = zeros((rows + 2 * pad, cols + 2 * pad))
        for i in range(rows):
            for j in range(cols):
                padded_img[i + pad][j + pad] = self.image[i][j]

        
        output_img = zeros((rows, cols))

        
        for i in range(rows):
            for j in range(cols):
                acc = 0.0
                for m in range(k_size):
                    for n in range(k_size):
                        acc += kernel[m][n] * padded_img[i + m][j + n]
                
                output_img[i][j] = min(max(int(acc), 0), 255)

        return output_img

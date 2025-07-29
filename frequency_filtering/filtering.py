from dip import zeros, fft2, ifft2, fftshift, ifftshift, uint8, min, max
import math


class Filtering:

    def __init__(self, image):
        """ initializes the variables for frequency filtering on an input image
        takes as input:
        image: the input image
        """
        self.image = image
        self.mask = self.get_mask

    def get_mask(self, shape):
        """ Computes a user-defined mask
        takes as input:
        shape: the shape of the mask to be generated
        rtype: a 2d numpy array with size of shape
        """
        rows, cols = shape
        mask = zeros(shape)

        
        for i in range(rows):
            for j in range(cols):
                mask[i][j] = 1

        
        blocked_points = [
        (280, 213),
        (243, 234),
        (231, 297),
        (268, 278)
    ]


        radius = 3  

        for center_row, center_col in blocked_points:
            for x in range(-radius, radius + 1):
                for y in range(-radius, radius + 1):
                    i = center_row + x
                    j = center_col + y
                    if 0 <= i < rows and 0 <= j < cols:
                        mask[i][j] = 0  

        return mask

    def post_process_image(self, image):
        """Post-processing to display DFTs and IDFTs
        takes as input:
        image: the image obtained from the inverse Fourier transform, forward Fourier transform, or filtered Fourier transform 
        return an image with full contrast stretch
        -----------------------------------------------------
        You can perform post-processing as needed. For example,
        1. You can perform log compression
        2. You can perform a full contrast stretch (fsimage)
        3. You can take negative (255 - fsimage)
        4. etc.
        """
        rows = len(image)
        cols = len(image[0])
        processed = zeros((rows, cols))

        
        for i in range(rows):
            for j in range(cols):
                processed[i][j] = math.log(1 + abs(image[i][j]))

        
        min_val = min(processed)
        max_val = max(processed)
        for i in range(rows):
            for j in range(cols):
                processed[i][j] = (processed[i][j] - min_val) / (max_val - min_val) * 255

        return processed.astype(uint8)

    def filter(self):
        """ Performs frequency filtering on an input image
        returns a filtered image, magnitude of frequency_filtering, magnitude of filtered frequency_filtering
        ----------------------------------------------------------
        You are allowed to use inbuilt functions to compute fft
        There are packages available in dip
        Steps:
        1. Compute the fft of the image
        2. shift the fft to center the low frequencies
        3. get the mask (write your code in the functions provided above) the functions can be called by self.filter(shape)
        4. filter the image frequency based on the mask (Convolution theorem)
        5. compute the inverse shift
        6. compute the inverse Fourier transform
        7. compute the magnitude
        8. You will need to do post-processing on the magnitude and depending on the algorithm (use post_process_image to write this code)
        Note: You do not have to do zero padding as discussed in class, the inbuilt functions take care of that
        filtered image, the magnitude of frequency_filtering, the magnitude of filtered frequency_filtering: Make sure all images being returned have grey scale full contrast stretch and dtype=uint8
        """
        # FFT
        fft_img = fft2(self.image)
        shifted_fft = fftshift(fft_img)

        # Geting mask
        mask = self.get_mask((len(self.image), len(self.image[0])))

        # Applying mask
        filtered_fft = shifted_fft * mask

        # Inverse shift and inverse FFT
        unshifted_fft = ifftshift(filtered_fft)
        inverse_img = ifft2(unshifted_fft)

        # Post-processing
        magnitude_original = self.post_process_image(shifted_fft)
        magnitude_filtered = self.post_process_image(filtered_fft)
        filtered_image = self.post_process_image(inverse_img)

        return [filtered_image, magnitude_original, magnitude_filtered]

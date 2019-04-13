import numpy as np
import cv2
from scipy import fftpack

IMAGE_PATH = "./image.tiff"
QUANTIZATION_MATRIX = [
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
]

def pad_image(image):
	width, height = image.shape
	width_padd, height_padd = 8 - width % 8, 8 - height % 8
	padded_image = np.zeros((width + width_padd, height + height_padd))
	# putting originial image in middle
	padded_image[width_padd//2:width + width_padd//2,
				 height_padd//2:height + height_padd//2] = image
	return padded_image

def jpeg_trans(image):

	def block_tansform(block):
		#applies DCT on this 8x8 block and then quantizes it with jpeg quantization matrix
		dct_block = fftpack.dct(fftpack.dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')
		return np.around(dct_block / QUANTIZATION_MATRIX)

	# normalize image
	image -= 127
	jpeg_image = np.zeros(image.shape)
	width, height = image.shape
	for i in range(0, width, 8):
		for j in range(0, height, 8):
			jpeg_image[i:i + 8, j:j + 8] = block_tansform(image[i:i + 8, j:j + 8])
	return jpeg_image

def inverse_jpeg_trans(jpeg_image):

	def block_inverse_transform(jpeg_block):
		# dequantises block and then applies IDCT on this 8x8 block
		jpeg_block *= QUANTIZATION_MATRIX
		return fftpack.idct(fftpack.idct(jpeg_block, axis=0, norm='ortho'), axis=1, norm='ortho')
	image = np.zeros(jpeg_image.shape)
	width, height = image.shape
	for i in range(0, width, 8):
		for j in range(0, height, 8):
			image[i:i + 8, j:j + 8] = block_inverse_transform(jpeg_image[i:i + 8, j:j + 8])
	return image + 127 # returns denormalized image

def main():
	image = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
	padded_image = pad_image(image)
	jpeg_image = jpeg_trans(padded_image)
	percentage_of_non_zero = np.sum(jpeg_image != 0) / np.multiply(*jpeg_image.shape) * 100
	print("only {}% of jpeg image is not zero".format(int(percentage_of_non_zero)))
	normal_image = inverse_jpeg_trans(jpeg_image)
	cv2.imwrite("retrans_image.tiff", normal_image)

main()

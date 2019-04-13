import cv2
import numpy as np
import matplotlib.pyplot as plt



def main():
    def show_image(name, image):
        cv2.imshow(name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    path = "simple_image.jpg"
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    show_image("original", image)

    transformed = np.fft.fft2(image)

    log = np.log2(1 + np.abs(transformed))

    show_image("transformed", log / np.max(log))

    maximum_transformed = np.max(np.abs(transformed))

    thresholds = [0.05, 0.01, 0.001, 0.0001, 0.00001, 0.000001]

    compression_ratios = []
    distortions = []

    for threshold in thresholds:
        compressed = (np.abs(transformed) > (threshold * maximum_transformed)) * transformed

        non_zero_percent = np.sum(np.abs(compressed) > 0) / np.multiply(*image.shape)
        compression_ratios.append(non_zero_percent)
        print("(threshold: {}) Non Zero Percent: {}".format(threshold, non_zero_percent))
        inversed_transformed = np.real(np.fft.ifft2(compressed))
        show_image("(threshold: {}) inversed_transformed".format(threshold), inversed_transformed)
        distortion = 100 * (np.linalg.norm(image - inversed_transformed, 'fro') ** 2) / (np.linalg.norm(image, 'fro') ** 2)
        distortions.append(distortion)
        print("(threshold: {}) distortion is: {}".format(threshold, distortion))

    plt.plot(distortions, compression_ratios)
    plt.xlabel(xlabel="distortion")
    plt.ylabel(ylabel="compression ratio")
    plt.show()


if __name__ == '__main__':
    main()

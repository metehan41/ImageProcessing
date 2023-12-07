
import numpy as np
import matplotlib.pyplot as plt
import cv2

def gaussianPyramid(image, count):
    pyramid = [image.astype(np.float32)]  # Save first image

    for i in range(count):
        image = cv2.GaussianBlur(image, (5, 5), 0)  # Apply Gaussian blur
        image = image[::2, ::2]  # Subsample by taking every L2 pixel
        pyramid.append(image.astype(np.float32))  # Save

    return pyramid

def laplacianPyramid(pyrmdGauss, count):
  minGaussian = pyrmdGauss[-1]  # Last gaussian is minimum-sized gaussian
  returnLaplacian = [minGaussian]  # Starts with minimum
  for i in range(count, 0, -1):
    size = (pyrmdGauss[i - 1].shape[1], pyrmdGauss[i - 1].shape[0])  # Calculate size to upsample
    gausUpscaled = cv2.resize(pyrmdGauss[i], size, interpolation = cv2.INTER_LINEAR)  # Upsample with calculated size
    lpl = cv2.subtract(pyrmdGauss[i-1], gausUpscaled)  # Subtract small but upsampled img from bigger img to obtain laplacian
    returnLaplacian.append(lpl)  # Save

  return returnLaplacian

def createLaplacianFromGaussian(L1):
    L1Gaussian = gaussianPyramid(L1, 300)  # Calculate gaussian pyramid for L1
    L1Laplacian = laplacianPyramid(L1Gaussian, 300)  # Calculate laplacian pyramid for L1
    
def createMaskGaussian(mask):
    maskGaussian = gaussianPyramid(mask, 300)  # Calculate gaussian pyramid for mask
    maskGaussian.reverse()  # Reverse for same order as laplacians
    return maskGaussian

def prepareMask(shape, x1, x2, y1, y2):
  mask = np.zeros((shape[0],shape[1],3), dtype='float32')  # Arrage an all 0's image with given size
  mask[x1 : x2, y1 : y2] = (1, 1, 1)  # Slightly brighten the blending part
  return mask

def shift_mask(mask, shift_x, shift_y):
    shifted_mask = np.roll(mask, (shift_x, shift_y), axis=(0, 1))
    return shifted_mask

def show_img_result():
    cv2.imshow()

def combine_pyramid_and_mask(finalLaplacian):
    fnlImg = finalLaplacian[0]
    finalImage = [fnlImg]  # Save reconstructed steps
    for i in range(300):
        size = (finalLaplacian[i + 1].shape[1], finalLaplacian[i + 1].shape[0])  # Calculate size to upsample
        fnlImg = cv2.pyrUp(fnlImg, dstsize = size)  # Upsample with calculated size
        # Upsample the image using cv2.resize()
        #upsampled_image = cv2.resize(fnlImg, size)
        fnlImg = cv2.add(finalLaplacian[i + 1], fnlImg)  # Add small but upsampled laplacian to bigger laplacian to obtain blended image
        finalImage.append(fnlImg)
    cv2.imshow(finalImage[300])

def main():
    print("Processing Image 1")
    L1 = cv2.imread("image_blending_with_pyramids/data/mona-lisa-tablosu.jpg")  # L1 image
    L2 = L1.copy()
    L2[320:360,350:500] = L1[40:80, 300:450]
    cv2.imshow("image 1 Raw", L1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
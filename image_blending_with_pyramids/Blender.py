import numpy as np
import matplotlib.pyplot as plt
import cv2

level = 150

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
    L1Gaussian = gaussianPyramid(L1, level)  # Calculate gaussian pyramid for L1
    L1Laplacian = laplacianPyramid(L1Gaussian, level)  # Calculate laplacian pyramid for L1
    return L1Laplacian
    
def createMaskGaussian(mask):
    maskGaussian = gaussianPyramid(mask, level)  # Calculate gaussian pyramid for mask
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

def combine_pyramid_and_mask(L1Laplacian, L2Laplacian, maskGaussian):
    finalLaplacian = []  # Save blended laplacians

    for L1L,L2L,maskG in zip(L1Laplacian, L2Laplacian, maskGaussian):  # For each laplacian in L1 and L2 and mask
        fnlLap = (L2L * maskG) + (L1L * (1 - maskG))
        finalLaplacian.append(fnlLap)

    fnlImg = finalLaplacian[0]
    finalImage = [fnlImg]  # Save reconstructed steps

    for i in range(level):
        size = (finalLaplacian[i + 1].shape[1], finalLaplacian[i + 1].shape[0])  # Calculate size to upsample
        fnlImg = cv2.pyrUp(fnlImg, dstsize = size)  # Upsample with calculated size
        # Upsample the image using cv2.resize()
        #upsampled_image = cv2.resize(fnlImg, size)
        fnlImg = cv2.add(finalLaplacian[i + 1], fnlImg)  # Add small but upsampled laplacian to bigger laplacian to obtain blended image
        finalImage.append(fnlImg)

    return finalImage[level]

def main():
    ################### IMAGE 1 ###################
    print("Processing Image 1")
    L1 = cv2.imread("/data/mona-lisa-tablosu.jpg")  # L1 image
    L2 = L1.copy()
    L2[320:360,350:500] = L1[40:80, 300:450]
    cv2.imwrite('/Result/Mona_Lisa/Raw.jpg',L1)
    cv2.imwrite('/Result/Mona_Lisa/withoutProcessed.jpg', L2)
    L1Laplacian = createLaplacianFromGaussian(L1)
    L2Laplacian = createLaplacianFromGaussian(L2)
    mask = prepareMask(L1.shape, 40, 80, 300, 450)
    image = L1.astype(np.uint8)
    mask_temp = mask.astype(np.uint8)
    masked_image = cv2.bitwise_and(image, image, mask=mask_temp[:,:,0])
    cv2.imwrite('/Result/Mona_Lisa/mask.jpg',masked_image)
    mask = shift_mask(mask, 280, 50)
    maskGaussian = createMaskGaussian(mask)
    finalImage = combine_pyramid_and_mask(L1Laplacian, L2Laplacian, maskGaussian)
    file_name = f'/Result/Mona_Lisa/finalImage{level}.jpg'
    cv2.imwrite(file_name,finalImage)

    ################### IMAGE 2 ###################

    print("Processing Image 2")
    L1 = cv2.imread("/data/apple-logo.jpg")  # L1 image
    L2 = cv2.imread("/data/apple-fruit.jpg")  # L2 image
    L2 = cv2.resize(L2, (L1.shape[1], L1.shape[0]))

    cv2.imwrite('/Result/Apple_Fruite_Or_Logo/Logo_Raw.jpg',L1)
    cv2.imwrite('/Result/Apple_Fruite_Or_Logo/Fruite_Raw.jpg', L2)

    L1Laplacian = createLaplacianFromGaussian(L1)
    L2Laplacian = createLaplacianFromGaussian(L2)

    mask = prepareMask(L1.shape, 0, L1.shape[0], 100, 250)

    image = L1.astype(np.uint8)
    mask_temp = mask.astype(np.uint8)
    masked_image = cv2.bitwise_and(image, image, mask=mask_temp[:,:,0])
    cv2.imwrite('/Result/Apple_Fruite_Or_Logo/mask.jpg',masked_image)

    maskGaussian = createMaskGaussian(mask)
    finalImage = combine_pyramid_and_mask(L1Laplacian, L2Laplacian, maskGaussian)
    file_name = f'/Result/Apple_Fruite_Or_Logo/finalImage{level}.jpg'
    cv2.imwrite(file_name,finalImage)

    ################### IMAGE 3 ###################

    print("Processing Image 3")
    L1 = cv2.imread("/data/cow.jpg")  # L1 image
    L2 = cv2.imread("/data/horse.jpg")  # L2 image

    L1 = L1[0:L2.shape[0], 0:L2.shape[1]]

    cv2.imwrite('/Result/Which_Animal_Is_That/cow_Raw.jpg',L1)
    cv2.imwrite('/Result/Which_Animal_Is_That/horse_Raw.jpg', L2)

    L1Laplacian = createLaplacianFromGaussian(L1)
    L2Laplacian = createLaplacianFromGaussian(L2)

    mask = prepareMask(L2.shape, 0, 500, 0, 400)

    image = L1.astype(np.uint8)
    mask_temp = mask.astype(np.uint8)
    masked_image = cv2.bitwise_and(image, image, mask=mask_temp[:,:,0])
    cv2.imwrite('/Result/Which_Animal_Is_That/mask.jpg',masked_image)

    maskGaussian = createMaskGaussian(mask)
    finalImage = combine_pyramid_and_mask(L1Laplacian, L2Laplacian, maskGaussian)
    file_name = f'/Result/Which_Animal_Is_That/finalImage{level}.jpg'
    cv2.imwrite(file_name,finalImage)

    ################### IMAGE 4 ###################

    print("Processing Image 4")

    L1 = cv2.imread("/data/istockphoto-1265147022-1024x1024.jpg")  # L1 image
    L2 = cv2.imread("/data/me.jpg")  # L2 image

    L2 = L2[600:600+L1.shape[0], 100:100+L1.shape[1]]

    cv2.imwrite('/Result/MeteInForrest/ForrestRaw.jpg',L1)
    cv2.imwrite('/Result/MeteInForrest/MeteRaw.jpg', L2)

    L1Laplacian = createLaplacianFromGaussian(L1)
    L2Laplacian = createLaplacianFromGaussian(L2)

    mask = prepareMask(L1.shape, 0, L1.shape[0], 400, 900)

    image = L1.astype(np.uint8)
    mask_temp = mask.astype(np.uint8)
    masked_image = cv2.bitwise_and(image, image, mask=mask_temp[:,:,0])
    cv2.imwrite('/Result/MeteInForrest/mask.jpg',masked_image)

    maskGaussian = createMaskGaussian(mask)
    finalImage = combine_pyramid_and_mask(L1Laplacian, L2Laplacian, maskGaussian)
    file_name = f'/Result/MeteInForrest/finalImage{level}.jpg'
    cv2.imwrite(file_name,finalImage)

    ################### IMAGE 5 ###################

    print("Processing Image 5")

    L1 = cv2.imread("/data/apple.jpg")  # L1 image
    L2 = cv2.imread("/data/orange.jpg")  # L2 image


    cv2.imwrite('/Result/OrangeOrApple/appleRaw.jpg',L1)
    cv2.imwrite('/Result/OrangeOrApple/orangeRaw.jpg', L2)

    L1Laplacian = createLaplacianFromGaussian(L1)
    L2Laplacian = createLaplacianFromGaussian(L2)

    mask = prepareMask(L1.shape, 0, L1.shape[0], L1.shape[0] // 2, L1.shape[0])

    image = L1.astype(np.uint8)
    mask_temp = mask.astype(np.uint8)
    masked_image = cv2.bitwise_and(image, image, mask=mask_temp[:,:,0])
    cv2.imwrite('/Result/OrangeOrApple/mask.jpg',masked_image)

    maskGaussian = createMaskGaussian(mask)
    finalImage = combine_pyramid_and_mask(L1Laplacian, L2Laplacian, maskGaussian)
    file_name = f'/Result/OrangeOrApple/finalImage{level}.jpg'
    cv2.imwrite(file_name,finalImage)



if __name__ == "__main__":
    main()
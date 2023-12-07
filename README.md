# Image Blending Project

## Introduction
In this project, our goal is to perform image blending using pyramid methods in image processing. We aim to achieve a smooth image blend, employing techniques such as Laplacian and Gaussian pyramids.

# History of Image Blending

The history of image blending is deeply rooted in the evolution of image processing and computer graphics. It has undergone significant transformations over time:

## Early Techniques
In the nascent stages of computer graphics, image blending primarily focused on seamlessly integrating multiple images or layers to create a composite image. Techniques like alpha blending were fundamental in this era.

## Photography and Editing Tools
As photography advanced, techniques emerged to merge or overlay multiple photographs for unique compositions. Traditional darkroom processes allowed photographers to blend images using multiple exposure techniques.

## Digital Era Advancements
The advent of digital image editing software, notably Adobe Photoshop and similar tools, revolutionized image blending. These tools introduced sophisticated blending modes, masks, and layering capabilities, enabling precise and seamless image combinations.

## Application in Computer Vision
In computer vision and image processing, blending became crucial for tasks like panoramic image stitching, enabling the creation of wider views through seamless combination of multiple images. Additionally, it found applications in medical imaging for merging different modalities or images for diagnosis and analysis.

## Advanced Blending Algorithms
Recent advancements in image processing led to the development of complex blending algorithms leveraging concepts like Laplacian and Gaussian pyramids. These algorithms aim to achieve smoother and more natural blending by considering local details and minimizing visible transitions between images.

## Artificial Intelligence and Blending
With the rise of AI and machine learning, image blending techniques have seen enhancements through neural network-based approaches, enabling more intelligent and context-aware blending.

Image blending has evolved significantly from its early roots, becoming an integral part of various fields, from photography and graphic design to computer vision and medical imaging, continually advancing through technological innovations and research breakthroughs.


## Problem Statement
The primary challenge lies in creating a seamlessly blended image after applying the blending process. We'll utilize the Image Pyramid method to address this issue, breaking it down into four main steps:

1. **Building Laplacian Pyramids for Each Image**
    - Utilizing functions like `gaussianPyramid` and `LaplacianPyramid`.
    - The `LaplacianPyramid` function constructs the Laplacian pyramid from a set of Gaussian pyramid levels, involving the usual process of reconstructing the Laplacian pyramid by upsampling Gaussian pyramid levels and subtracting from the previous level.

2. **Building a Gaussian Pyramid for Each Region Mask**
    - Using the `gaussianPyramid` function to generate a Gaussian pyramid of masks.
    - Creating a mask region with white for specific areas and black for others by combining our image and the original image.

3. **Blending Each Level of the Pyramid Using Region Masks**
    - Employing a given formula for this step.

4. **Collapsing the Pyramid to Obtain the Final Blended Image**

## Demonstration of Hyperparameters for 5 Images

### Image 1
- Displaying the results for different pyramid levels:
  <div style="display: flex; justify-content: center;">
  <div style="text-align: center; margin-right: 10px;">
    <img src="https://github.com/metehan41/ImageProcessing/blob/master/image_blending_with_pyramids/Result/Mona_Lisa/finalImage1.jpg" alt="Image 1" style="width: 50;">
    <p>Pyramid Level 1</p>
  </div>
  <div style="text-align: center; margin-left: 10px;">
    <img src="https://github.com/metehan41/ImageProcessing/blob/master/image_blending_with_pyramids/Result/Mona_Lisa/finalImage3.jpg" alt="Image 2" style="width: 50;">
    <p>Pyramid Level 3</p>
  </div>
  <div style="display: flex; justify-content: center;">
  <div style="text-align: center; margin-right: 10px;">
    <img src="https://github.com/metehan41/ImageProcessing/blob/master/image_blending_with_pyramids/Result/Mona_Lisa/finalImage5.jpg" alt="Image 1" style="width: 50;">
    <p>Pyramid Level 5</p>
  </div>
  <div style="text-align: center; margin-left: 10px;">
    <img src="https://github.com/metehan41/ImageProcessing/blob/master/image_blending_with_pyramids/Result/Mona_Lisa/finalImage10.jpg" alt="Image 2" style="width: 50;">
    <p>Pyramid Level 10</p>
  </div>
  <div style="display: flex; justify-content: center;">
  <div style="text-align: center; margin-right: 10px;">
    <img src="https://github.com/metehan41/ImageProcessing/blob/master/image_blending_with_pyramids/Result/Mona_Lisa/finalImage50.jpg" alt="Image 1" style="width: 50;">
    <p>Pyramid Level 50</p>
  </div> 
    <div style="display: flex; justify-content: center;">
    <div style="text-align: center; margin-right: 10px;">
    <img src="https://github.com/metehan41/ImageProcessing/blob/master/image_blending_with_pyramids/Result/Mona_Lisa/finalImage100.jpg" alt="Image 1" style="width: 50;">
    <p>Pyramid Level 100</p>
  </div>
  <div style="text-align: center; margin-left: 10px;">
    <img src="https://github.com/metehan41/ImageProcessing/blob/master/image_blending_with_pyramids/Result/Mona_Lisa/finalImage150.jpg" alt="Image 2" style="width: 50;">
    <p>Pyramid Level 150</p>
  </div>
</div>

[You can access other resulter under result file]


## File Structure
- `README.txt`: Details about the assignment and a Google Drive link (without login) containing all images (input, mask, blended).
- `code/`: Directory with all code files (`.py`).
- `report.pdf`: A PDF report summarizing the project.
  [Download My PDF File](https://drive.google.com/your_file_link)

## References
- "Pyramid methods in image processing, E. H. Adelson, C. H. Anderson, J. R. Bergen, P. J. Burt, J. M. Ogden,1984"

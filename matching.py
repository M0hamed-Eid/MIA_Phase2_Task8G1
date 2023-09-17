import numpy as np
import cv2

# Block Matching Function
def block_matching(left_image, right_image, block_size=5, max_disparity=64):
    height, width = left_image.shape[:2]
    depth_map = np.zeros_like(left_image, dtype=np.uint8)

    half_block = block_size // 2
    
    # Iterates through each pixel in the left image within the vali range for block matching
    # For each pixel in the left image, a block of pixels is extracted.
    # Disparity represents the horizontal offset between the left and the right images and
    # the code iterates through a range of disparities 'd' from 0 to 'max_disparity'
    # Caclulates the poisition 'x_r' in the right image based on the current disparity.
    # 'ssd' is computed between the left and right blocks and the disparity with the minimum ssd
    # is selected as the best disparity, then it is stored in the 'depth_map'.

    for y in range(half_block, height - half_block):
        for x in range(half_block, width - half_block):
            left_block = left_image[y - half_block:y + half_block + 1, x - half_block:x + half_block + 1]

            min_ssd = float('inf')
            best_disparity = 0

            for d in range(max_disparity):
                x_r = x - d
                
                if x_r - half_block < 0:
                    break

                right_block = right_image[y - half_block:y + half_block + 1, x_r - half_block:x_r + half_block + 1]

                if right_block.shape != left_block.shape:
                    break
                # ssd calculation
                ssd = np.sum((left_block - right_block) ** 2)
                # checking for min_ss
                if ssd < min_ssd:
                    min_ssd = ssd
                    best_disparity = d

            depth_map[y, x] = best_disparity # storing the best disparity

    return depth_map

# Code Excution
if __name__ == "__main__":
    left_image = cv2.imread("stereo_left.png", cv2.IMREAD_GRAYSCALE)
    right_image = cv2.imread("stereo_right.png", cv2.IMREAD_GRAYSCALE)

    depth_map = block_matching(left_image, right_image)

    cv2.imwrite("depth_map.png", depth_map)
    cv2.imshow("Depth Map", depth_map)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
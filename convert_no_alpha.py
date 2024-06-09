import cv2
import os
import numpy as np


def get_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"Error: Unable to load image from {image_path}")

    if image.shape[2] == 4:  # Check if the image has an alpha channel
        print("image has alpha")
        alpha_channel = image[:, :, 3]
        _, mask = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)
        color = image[:, :, :3]
        white_background = np.ones_like(color, dtype=np.uint8) * 255
        image = cv2.bitwise_not(
            cv2.bitwise_not(color, mask=mask) + cv2.bitwise_not(white_background, mask=cv2.bitwise_not(mask)))

    return image


base_folder = '/Users/diegosiqueira/Playground/numbers/tests'
base_folder_out = '/Users/diegosiqueira/Playground/numbers/tests_out'

base_images = []
for filename in os.listdir(base_folder):
    base_image_path = os.path.join(base_folder, filename)
    base_image = get_image(base_image_path)

    output_path = os.path.join(base_folder_out, filename)
    cv2.imwrite(output_path, base_image)

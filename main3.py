import cv2
import numpy as np
import os


def get_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"Error: Unable to load image from {image_path}")

    if image.shape[2] == 4:  # Check if the image has an alpha channel
        alpha_channel = image[:, :, 3]
        _, mask = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)
        color = image[:, :, :3]
        white_background = np.ones_like(color, dtype=np.uint8) * 255
        image = cv2.bitwise_not(
            cv2.bitwise_not(color, mask=mask) + cv2.bitwise_not(white_background, mask=cv2.bitwise_not(mask)))

    return image


def split_into_quadrants(image):
    height, width = image.shape[:2]
    mid_x, mid_y = width // 2, height // 2
    return [
        image[0:mid_y, 0:mid_x],  # Top-Left -> Tens
        image[0:mid_y, mid_x:width],  # Top-Right -> Units
        image[mid_y:height, 0:mid_x],  # Bottom-Left -> Thousands
        image[mid_y:height, mid_x:width]  # Bottom-Right -> Hundreds
    ]


def mirror_quadrants(quadrants):
    return [
        cv2.flip(quadrants[0], 1),  # Mirrored horizontally
        quadrants[1],  # Not mirrored
        cv2.flip(quadrants[2], -1),  # Mirrored both vertically and horizontally
        cv2.flip(quadrants[3], 0)  # Mirrored vertically
    ]


def compare_images(image1, image2, threshold=30):
    if image1.shape != image2.shape:
        return False
    cropped_image1 = image1[:, 3:]
    cropped_image2 = image2[:, 3:]
    difference = cv2.absdiff(cropped_image1, cropped_image2)
    _, thresh = cv2.threshold(difference, threshold, 255, cv2.THRESH_BINARY)
    return np.count_nonzero(thresh) == 0


def find_matching_quadrant(image_path, base_folder):
    image = get_image(image_path)
    quadrants = split_into_quadrants(image)
    mirrored_quadrants = mirror_quadrants(quadrants)

    base_images = []
    for filename in os.listdir(base_folder):
        base_image_path = os.path.join(base_folder, filename)
        base_image = get_image(base_image_path)
        value = int(os.path.splitext(filename)[0].split('_')[1])
        base_images.append((base_image, value))

    total_sum = 0
    quadrant_values = [10, 1, 1000, 100]

    for i, quadrant in enumerate(mirrored_quadrants):
        for base_image, base_value in base_images:
            if compare_images(quadrant, base_image):
                total_sum += base_value * quadrant_values[i]

    print(f"Total sum: {total_sum}")


# Example usage:
image_path = '/Users/diegosiqueira/Playground/numbers/tests/9999.png'
base_folder = '/Users/diegosiqueira/Playground/numbers/base'
find_matching_quadrant(image_path, base_folder)

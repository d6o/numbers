import cv2
import numpy as np
import os


# Load an image and replace the transparent background with white
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


# Split an image into four quadrants
def split_into_quadrants(image):
    height, width = image.shape[:2]
    mid_x, mid_y = width // 2, height // 2

    quadrants = {
        'tens': image[0:mid_y, 0:mid_x],  # Top-Left -> Tens
        'units': image[0:mid_y, mid_x:width],  # Top-Right -> Units
        'thousands': image[mid_y:height, 0:mid_x],  # Bottom-Left -> Thousands
        'hundreds': image[mid_y:height, mid_x:width]  # Bottom-Right -> Hundreds
    }

    return quadrants


# Mirror the quadrants as specified
def mirror_quadrants(quadrants):
    mirrored_quadrants = {
        'tens': cv2.flip(quadrants['tens'], 1),  # Mirrored horizontally
        'units': quadrants['units'],  # Not mirrored
        'thousands': cv2.flip(quadrants['thousands'], -1),  # Mirrored both vertically and horizontally
        'hundreds': cv2.flip(quadrants['hundreds'], 0)  # Mirrored vertically
    }

    return mirrored_quadrants


# Save the quadrants to the output folder
def save_quadrants(quadrants, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for name, quadrant in quadrants.items():
        quadrant_path = os.path.join(output_folder, f'quadrant_{name}.png')
        cv2.imwrite(quadrant_path, quadrant)
        print(f'Saved {quadrant_path}')


# Compare two images using absolute difference, ignoring the first 3 pixels on the left
def compare_images(image1, image2, threshold=30):
    if image1.shape != image2.shape:
        return False
    # Ignore the first 3 pixels on the left
    cropped_image1 = image1[:, 3:]
    cropped_image2 = image2[:, 3:]
    difference = cv2.absdiff(cropped_image1, cropped_image2)
    _, thresh = cv2.threshold(difference, threshold, 255, cv2.THRESH_BINARY)
    return np.count_nonzero(thresh) == 0


# Find matching quadrants with base images
def find_matching_quadrant(image_path, base_folder, output_folder):
    image = get_image(image_path)
    quadrants = split_into_quadrants(image)
    mirrored_quadrants = mirror_quadrants(quadrants)
    save_quadrants(mirrored_quadrants, output_folder)

    base_images = []
    for filename in os.listdir(base_folder):
        base_image_path = os.path.join(base_folder, filename)
        base_image = get_image(base_image_path)
        value = int(os.path.splitext(filename)[0].split('_')[1])
        base_images.append((filename, base_image, value))

    matching_base_images = {}
    quadrant_values = {'tens': 10, 'units': 1, 'thousands': 1000, 'hundreds': 100}
    total_sum = 0

    for name, quadrant in mirrored_quadrants.items():
        for base_filename, base_image, base_value in base_images:
            if compare_images(quadrant, base_image):
                match_value = base_value * quadrant_values[name]
                total_sum += match_value
                if base_filename not in matching_base_images:
                    matching_base_images[base_filename] = []
                matching_base_images[base_filename].append((name, match_value))

    if not matching_base_images:
        print("No matching quadrant found")
    else:
        for base_filename, matches in matching_base_images.items():
            match_details = ', '.join([f"{quadrant} (value: {value})" for quadrant, value in matches])
            print(f"{base_filename} matched with quadrants: {match_details}")

    print(f"Total sum: {total_sum}")


# Example usage:
image_path = '/Users/diegosiqueira/Playground/numbers/tests/.png'
base_folder = '/Users/diegosiqueira/Playground/numbers/base'
output_folder = '/Users/diegosiqueira/Playground/numbers/out'

find_matching_quadrant(image_path, base_folder, output_folder)

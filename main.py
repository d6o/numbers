import cv2
import numpy as np
import os


def split_into_quadrants(image):
    height, width = image.shape[:2]
    mid_x, mid_y = width // 2, height // 2

    quadrants = [
        image[0:mid_y, 0:mid_x],  # Top-Left -> Tens
        image[0:mid_y, mid_x:width],  # Top-Right -> Units
        image[mid_y:height, 0:mid_x],  # Bottom-Left -> Thousands
        image[mid_y:height, mid_x:width]  # Bottom-Right -> Hundreds
    ]

    return quadrants


def mirror_quadrants(quadrants):
    mirrored_quadrants = [
        cv2.flip(quadrants[0], 1),  # Top-Left -> Tens mirrored horizontally
        quadrants[1],  # Top-Right -> Units not mirrored
        cv2.flip(quadrants[2], -1),  # Bottom-Left -> Thousands mirrored both vertically and horizontally
        cv2.flip(quadrants[3], 0)  # Bottom-Right -> Hundreds mirrored vertically
    ]

    return mirrored_quadrants


def save_quadrants(quadrants, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    quadrant_names = ['tens', 'units', 'thousands', 'hundreds']
    for i, quadrant in enumerate(quadrants):
        quadrant_path = os.path.join(output_folder, f'quadrant_{quadrant_names[i]}.png')
        cv2.imwrite(quadrant_path, quadrant)
        print(f'Saved {quadrant_path}')


def compare_images(image1, image2):
    if image1.shape != image2.shape:
        return False
    difference = cv2.subtract(image1, image2)
    return np.all(difference == 0)


def get_image(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Error: Unable to load image from {image_path}")
        return

    # Replace transparent background with white
    if image.shape[2] == 4:  # Check if the image has an alpha channel
        alpha_channel = image[:, :, 3]
        _, mask = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)
        color = image[:, :, :3]
        white_background = np.ones_like(color, dtype=np.uint8) * 255
        image = cv2.bitwise_not(
            cv2.bitwise_not(color, mask=mask) + cv2.bitwise_not(white_background, mask=cv2.bitwise_not(mask)))

    return image


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
    quadrant_names = ['tens', 'units', 'thousands', 'hundreds']
    quadrant_values = [10, 1, 1000, 100]
    total_sum = 0

    for i, quadrant in enumerate(mirrored_quadrants):
        for base_filename, base_image, base_value in base_images:
            if compare_images(quadrant, base_image):
                match_value = base_value * quadrant_values[i]
                total_sum += match_value
                if base_filename not in matching_base_images:
                    matching_base_images[base_filename] = []
                matching_base_images[base_filename].append((quadrant_names[i], match_value))

    if not matching_base_images:
        print("No matching quadrant found")
    else:
        for base_filename, matches in matching_base_images.items():
            match_details = ', '.join([f"{quadrant} (value: {value})" for quadrant, value in matches])
            print(f"{base_filename} matched with quadrants: {match_details}")

    print(f"Total sum: {total_sum}")


# Example usage:
image_path = '/tests/dcode-5678.png'
base_folder = '/Users/diegosiqueira/Playground/numbers/base'
output_folder = '/Users/diegosiqueira/Playground/numbers/out'

find_matching_quadrant(image_path, base_folder, output_folder)

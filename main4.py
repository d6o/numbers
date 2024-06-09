import argparse
import cv2
import numpy as np
import os


def get_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"Error: Unable to load image from {image_path}")

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


# Save the quadrants to the output folder
def save_quadrants(quadrants, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, quadrant in enumerate(quadrants):
        output_path = os.path.join(output_folder, f"quadrant_{i}.png")
        cv2.imwrite(output_path, quadrant)


def find_matching_quadrant(image_path, base_folder):
    image = get_image(image_path)
    quadrants = split_into_quadrants(image)
    mirrored_quadrants = mirror_quadrants(quadrants)
    save_quadrants(mirrored_quadrants, "/Users/diegosiqueira/Playground/numbers/out")

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a Cistercian number image.")
    parser.add_argument("image_path", type=str, help="Path to the Cistercian number image")

    base_folder = '/Users/diegosiqueira/Playground/numbers/base'

    args = parser.parse_args()

    find_matching_quadrant(args.image_path, base_folder)
